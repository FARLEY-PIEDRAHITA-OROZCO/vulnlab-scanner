vulnlab-scanner/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada
│   ├── cli.py               # Manejo de argumentos CLI
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── base.py          # Lógica base del scanner
│   │   ├── xss.py           # Módulo de XSS
│   │   ├── sqli.py          # Módulo de SQL Injection
│   │   └── headers.py       # Seguridad en headers
│   │
│   └── utils/
│       ├── logger.py        # Salida en consola
│       └── helpers.py
│
├── requirements.txt
└── README.md