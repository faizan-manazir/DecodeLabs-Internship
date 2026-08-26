import logging
from flask import Blueprint, current_app, jsonify, request
from services.crypto_service import CryptoService

api_bp = Blueprint("api", __name__)
crypto_service = CryptoService()
logger = logging.getLogger(__name__)

def _payload():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Request must contain valid JSON.")
    algorithm = data.get("algorithm")
    text = data.get("text")
    key = data.get("key")
    if not isinstance(algorithm, str) or not algorithm:
        raise ValueError("An algorithm is required.")
    if not isinstance(text, str):
        raise ValueError("Text input is required.")
    if len(text) > current_app.config["MAX_TEXT_LENGTH"]:
        raise ValueError("Text input exceeds the allowed size.")
    if key is not None and not isinstance(key, str):
        raise ValueError("Key must be text.")
    return algorithm, text, key

@api_bp.get("/algorithms")
def algorithms():
    return jsonify({"success": True, "algorithms": crypto_service.get_algorithms_info()})

@api_bp.post("/encrypt")
def encrypt():
    try:
        algorithm, text, key = _payload()
        return jsonify({"success": True, "operation": "encrypt", "algorithm": algorithm,
                        "result": crypto_service.encrypt(algorithm, text, key)})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        logger.exception("Encryption error")
        return jsonify({"success": False, "error": "Encryption failed. Please check your input."}), 500

@api_bp.post("/decrypt")
def decrypt():
    try:
        algorithm, text, key = _payload()
        return jsonify({"success": True, "operation": "decrypt", "algorithm": algorithm,
                        "result": crypto_service.decrypt(algorithm, text, key)})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        logger.exception("Decryption error")
        return jsonify({"success": False, "error": "Decryption failed. Please check your input and key."}), 500


@api_bp.post("/compare")
def compare():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            raise ValueError("Request must contain valid JSON.")
        text = data.get("text")
        selected = data.get("algorithms")
        keys = data.get("keys", {})
        if not isinstance(text, str) or not text:
            raise ValueError("Text input is required.")
        if not isinstance(selected, list) or not selected:
            raise ValueError("Select at least one algorithm.")
        if len(selected) > 8:
            raise ValueError("Too many algorithms selected.")
        results = []
        for algorithm_id in selected:
            algo = crypto_service.algorithms.get(algorithm_id)
            if not algo:
                continue
            key = keys.get(algorithm_id, "")
            if algo.requires_key and not key:
                results.append({"algorithm": algorithm_id, "name": algo.name, "success": False,
                                "error": "A key is required for this algorithm."})
                continue
            try:
                result = crypto_service.encrypt(algorithm_id, text, key)
                results.append({"algorithm": algorithm_id, "name": algo.name, "category": algo.category,
                                "security_level": algo.security_level, "success": True,
                                "result": result, "output_length": len(result)})
            except ValueError as exc:
                results.append({"algorithm": algorithm_id, "name": algo.name, "success": False, "error": str(exc)})
        return jsonify({"success": True, "results": results})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception:
        logger.exception("Comparison error")
        return jsonify({"success": False, "error": "Comparison failed. Please check your input."}), 500
