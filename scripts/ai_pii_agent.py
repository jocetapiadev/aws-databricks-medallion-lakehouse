import json

def agente_clasificador_pii(columna_nombre, muestra_datos):
    """
    Agente DataOps (Guardrail IA) que evalúa si una columna 
    contiene PII antes de procesar la capa Silver.
    """
    pii_keywords = ["email", "correo", "phone", "rut", "dni", "ssn"]
    
    is_pii = any(key in columna_nombre.lower() for key in pii_keywords)
    
    return {
        "column": columna_nombre,
        "is_pii_detected": is_pii,
        "recommended_action": "HASH_SHA256" if is_pii else "PASS_THROUGH"
    }

if __name__ == "__main__":
    resultado = agente_clasificador_pii("email_usuario", ["test@domain.com"])
    print(f"Decisión del Agente IA DataOps: {json.dumps(resultado, indent=2)}")
