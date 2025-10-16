def api_call(query):

    import os
    from dotenv import load_dotenv
    from groq import Groq
    import json

    # Carica le variabili dal file .env
    load_dotenv()

    # Recupera la chiave dalla variabile d'ambiente
    api_key = os.getenv("GROQ_API_KEY")

    # Recupero schema db
    with open("db_scheme.txt", "r", encoding="utf-8") as f:
        scheme = f.read()

    # Crea il client Groq
    client = Groq()

    # Prompt engineering
    prompt = """Interpreta la richiesta dell'utente: """ + query + """\nAnalizza lo schema e la struttura del database SQLite: """ + scheme + """"\nValuta la probabilità che la richiesta dell'utente sia inerente rispetto allo schema del database. Se non la ritieni inerente, passa allo STEP FINALE. Qualora invece la ritenessi inerente, che informazioni vorrebbe poter ottenere l'utente o che operazioni vorrebbe eseguire sul database? In questo caso, contempla vaghezza e pressapochismo dell'utente. Se ti risulta comunque una richiesta strana, passa allo STEP FINALE. Altrimenti ragiona, formula la query in linguagio SQLite che sia probabilmente quella più adatta relativamente al contestuale schema del database e alla richiesta dell'utente. STEP FINALE: rispondi SOLO con JSON in questo formato:
    {
      "query": "query formulata in linguaggio SQLite" oppure "⚠️ Warning: richiesta ambigua o non inerente!",
      "disamina": "breve descrizione del tuo processo decisionale e breve delucidazione sulla strutturazione della query e dei relativi comandi SQLite utilizzati"
    }"""


    # Invia la richiesta con JSON mode
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Rispondi SEMPRE con JSON valido. Non aggiungere testo prima o dopo il JSON."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
        ],
        temperature= 0.4,
        max_completion_tokens=1024,
        top_p= 0.95,
        reasoning_effort="medium",
        stream=False,
        response_format={"type": "json_object"}
    )


    # Parsa il JSON dalla risposta
    response_json = json.loads(completion.choices[0].message.content)

    # Salva come file JSON formattato
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(response_json, f, indent=2, ensure_ascii=False)