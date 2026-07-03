from datetime import date

SFATURI = [
    "🔒 Folosește parole diferite pentru fiecare cont important.",
    "📧 Nu deschide atașamente din e-mailuri necunoscute.",
    "🛡️ Activează autentificarea în doi pași ori de câte ori este posibil.",
    "💻 Blochează calculatorul când te îndepărtezi de birou.",
    "🌐 Verifică întotdeauna adresa site-ului înainte de autentificare.",
    "📱 Actualizează periodic sistemul de operare și aplicațiile.",
    "⚠️ Nu introduce date personale pe site-uri nesigure.",
    "📂 Fă copii de siguranță (backup) pentru fișierele importante.",
    "🔑 Nu transmite parole prin e-mail sau aplicații de mesagerie.",
    "🦠 Folosește un antivirus actualizat.",
    "🚫 Nu conecta stick-uri USB necunoscute la calculator.",
    "📶 Evită conectarea la rețele Wi-Fi publice fără VPN.",
    "👀 Verifică expeditorul înainte de a răspunde unui e-mail.",
    "📄 Citește cu atenție permisiunile cerute de aplicații.",
    "🛑 Dacă ceva pare suspect, raportează imediat administratorului IT."
]


def obtine_sfatul_zilei() -> str:
    index = date.today().toordinal() % len(SFATURI)
    return SFATURI[index]