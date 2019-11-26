# Configuration
## IntelliJ & venv...
- IntelliJ → Project Structure → Project SDK → New → Python Virtual Environment
  - Python 3.8
  - Dans `.\cassebrique\venv`
  
N'arrivant pas à installer les packages depuis IntelliJ, je l'ai fait de la manière suivante: 
- `cd .\cassebrique\venv\Scripts`
- `python -m pip install -U --force-reinstall pip` à lancer deux fois si ne fonctionne pas à la première, cf. https://github.com/pypa/pip/issues/5820, commentaire de fingerman
- `pip install pygame`

## UnitTests
Pas de TDD ni même de bêtes tests unitaires : ce n'est pas encore dans la leçon.