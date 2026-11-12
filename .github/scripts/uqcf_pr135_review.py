"""One Gemini generation on exact full PR135 source text; no scientific execution."""
import json
import os
from pathlib import Path
import urllib.request
from uqcf_pr135_integrity import ROOT, build_prompt, input_manifest, load_sources, parse_json, require, run_identity, sha256, write_json

MODEL = 'gemini-3.1-pro-preview'

def parse_response(raw):
    response = parse_json(raw)
    require(not response.get('promptFeedback', {}).get('blockReason'), 'Blocked prompt')
    candidates = response.get('candidates')
    require(isinstance(candidates, list) and len(candidates) == 1, 'Expected exactly one candidate')
    candidate = candidates[0]
    require(candidate.get('finishReason') == 'STOP', 'Incomplete review response')
    parts = candidate.get('content', {}).get('parts', [])
    require(isinstance(parts, list), 'Invalid response parts')
    texts = [p['text'] for p in parts if not p.get('thought', False) and isinstance(p.get('text'), str)]
    require(bool(texts), 'No visible review text')
    answer = '\n'.join(texts).strip().encode('utf-8')
    verdict = parse_json(answer)
    require(isinstance(verdict, dict) and verdict.get('verdict') in ('ACCEPTED', 'REVISE', 'FAIL'), 'Invalid verdict')
    require(all(isinstance(verdict.get(k), list) for k in ('findings', 'missing_assumptions', 'counterexamples', 'limitations', 'constructive_analysis')), 'Invalid review arrays')
    require(verdict.get('native_bridge_status') in ('NOT_DERIVED', 'DERIVED_FROM_SOURCES') and isinstance(verdict.get('next_native_obligation'), str), 'Invalid claim scope')
    returned = response.get('modelVersion')
    require(isinstance(returned, str) and (returned == MODEL or returned.startswith(MODEL + '-')), 'Missing or unexpected returned model')
    return answer, verdict, returned

def accepted(verdict):
    require(verdict['verdict'] == 'ACCEPTED' and all(verdict[k] == [] for k in ('findings', 'missing_assumptions', 'counterexamples')), 'Review not accepted or unresolved substantive finding')

def call_model(out, key, prompt, opener=urllib.request.urlopen):
    endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/' + MODEL
    headers = {'x-goog-api-key': key}
    with opener(urllib.request.Request(endpoint, headers=headers, method='GET'), timeout=60) as response:
        metadata_raw = response.read()
    (out / 'model_metadata.json').write_bytes(metadata_raw)
    metadata = parse_json(metadata_raw)
    require(metadata.get('name') == 'models/' + MODEL and 'generateContent' in metadata.get('supportedGenerationMethods', []), 'Requested model unavailable')
    body = {'contents': [{'role': 'user', 'parts': [{'text': prompt.decode('utf-8')}]}],
            'generationConfig': {'temperature': 0, 'maxOutputTokens': 32768, 'responseMimeType': 'application/json'}}
    request_raw = (json.dumps(body, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8')
    (out / 'request.json').write_bytes(request_raw)
    request = urllib.request.Request(endpoint + ':generateContent', data=request_raw, headers={**headers, 'Content-Type': 'application/json'}, method='POST')
    with opener(request, timeout=600) as response:
        raw = response.read()
    (out / 'response.json').write_bytes(raw)
    return raw

def main():
    out = Path('pr135_review'); out.mkdir(exist_ok=True)
    manifest = {'status': 'INCOMPLETE', 'model_requested': MODEL, 'model_returned': None, 'generation_calls_maximum': 1}
    try:
        run = run_identity(ROOT); manifest.update(run)
        lock, _ = load_sources(ROOT); inputs = input_manifest(ROOT, lock)
        integrity = Path('pr135_integrity')
        evidence = parse_json((integrity / 'integrity.json').read_bytes())
        require(evidence.get('status') == 'PASS' and evidence.get('scientific_execution') is False and all(evidence.get(k) == v for k, v in run.items()), 'Integrity not passed for exact run')
        for name, expected in (('input_manifest', inputs), ('source_manifest', lock)):
            raw = (integrity / (name + '.json')).read_bytes()
            require(sha256(raw) == evidence.get(name + '_sha256') and parse_json(raw) == expected, 'Integrity manifest differs')
        manifest['integrity_artifacts'] = {p.name: sha256(p.read_bytes()) for p in sorted(integrity.iterdir()) if p.is_file()}
        write_json(out / 'input_manifest.json', inputs)
        prompt = build_prompt(ROOT, lock)
        require(sha256(prompt) == evidence.get('prompt_sha256'), 'Prompt differs from integrity check')
        (out / 'prompt.txt').write_bytes(prompt)
        raw = call_model(out, os.environ['GEMINI_API_KEY'], prompt)
        answer, verdict, returned = parse_response(raw)
        (out / 'review.txt').write_bytes(answer)
        write_json(out / 'verdict.json', verdict)
        manifest.update(model_returned=returned, status=verdict['verdict'])
        accepted(verdict)
        print('Independent Gemini whole-packet source review ACCEPTED; raw evidence retained.')
    except Exception as exc:
        write_json(out / 'failure.json', {'status': 'REVIEW_NOT_ACCEPTED_OR_INFRASTRUCTURE_FAILURE', 'error_type': type(exc).__name__, 'http_status': getattr(exc, 'code', None)})
        raise SystemExit('Review incomplete or not accepted; sanitized evidence retained, no secrets printed.')
    finally:
        manifest['artifact_hashes'] = {p.name: sha256(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file() and p.name != 'manifest.json'}
        write_json(out / 'manifest.json', manifest)

if __name__ == '__main__':
    main()
