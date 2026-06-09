# stopwords.py

STOP_WORDS_ES = {
    # 1. Artículos y Pronombres
    "algo", "alguien", "algunas", "algunos", "cual", "cualquier", "él", "ella", "ellas", 
    "ello", "ellos", "el", "la", "las", "lo", "los", "me", "mi", "mí", "mía", "mías", 
    "mío", "míos", "mis", "nada", "nos", "nosotras", "nosotros", "nuestra", "nuestras", 
    "nuestro", "nuestros", "os", "otra", "otras", "otro", "otros", "qué", "que", "quien", 
    "quienes", "se", "su", "sus", "suya", "suyas", "suyo", "suyos", "te", "ti", "todo", 
    "todos", "tu", "tú", "tus", "tuya", "tuyas", "tuyo", "tuyos", "un", "una", "unas", 
    "uno", "unos", "vosotras", "vosotros", "yo", "este", "esta", "estos", "estas", 
    "ese", "esa", "esos", "esas", "esto", "eso", "le", "les",

    # 2. Preposiciones y Conjunciones
    "a", "al", "ante", "aunque", "como", "con", "contra", "cuando", "de", "del", 
    "desde", "donde", "durante", "e", "en", "entre", "hasta", "mas", "más", "ni", 
    "o", "para", "pero", "por", "porque", "pues", "según", "sin", "sobre", "y", "ya",

    # 3. Verbos Auxiliares y Comunes (ser, estar, tener, ir, hacer, etc.)
    "crear", "creo", "dejo", "editó", "era", "es", "está", "estaba", "están", "estar", "estoy", 
    "fue", "fueron", "ha", "había", "habían", "habia", "hace", "hacer", "hacerlo", 
    "haciendo", "hago", "han", "hay", "haya", "he", "hemos", "hice", "hizo", "mando", "parece", 
    "paso", "pongo", "puede", "puedo", "puse", "quieren", "sea", "ser", "sido", "son", "tenía", 
    "tenían", "tener", "tengo", "tiene", "tienen", "usar", "va", "vamos", "veo", "vemos", 
    "ver", "vi", "viendo", "voy",

    # 4. Adverbios, Tiempo y Cantidades
    "ahí", "ahi", "ahora", "antes", "así", "asi", "bien", "bueno", "cada", "claro", 
    "después", "directamente", "domingo", "entonces", "final", "hora", "hoy", "igual", 
    "mañana", "mal", "mejor", "mucho", "muchos", "muy", "no", "poco", "sí", "si", "solo", 
    "tal", "también", "tambien", "tanto", "tarde", "ultima", "verdad",

    # 5. Jerga de WhatsApp y Expresiones Informales
    "ah", "ajaja", "ajja", "ajsja", "bah", "buenas", "dale", "drama", "eh", "gente",
    "finde", "ja", "jaja", "jajaj", "jajaja", "jajajaja", "joya", "listo", "multimedia", 
    "oh", "ok", "okey", "omitido", "onda", "sisi", "tipo", "toque", "tranqui", "xd",

    # 6. Relleno y Palabras Generales
    "com", "cosa", "cosas", "cuenta", "forma", "idea"
}
