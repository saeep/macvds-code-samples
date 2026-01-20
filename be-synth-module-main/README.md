# *Setup Guide*  

The *Soundfont Generator App* allows users to generate synthesized reed harmonium sample-based SF2 files, configured with tuning based on either *Western* or *Hindustani* systems. The Western tuning follows standard *12-TET mappings, while the Hindustani tuning allows **shruti frequencies* to be mapped to keyboard keys. Users can either use default shruti ratios or provide custom ratios.

Users can input a *base key* along with a *base frequency*, select the desired shrutis, and generate an SF2 file.


## *Prerequisites*  
Before proceeding, ensure you have the following installed on your system:  

- *Python 3.x* (Download from [python.org](https://www.python.org/))  
- *Git* (Download from [git-scm.com](https://git-scm.com/))  


## *Installation Steps*  

### *1. Clone the Repository*  
To clone the repository, open a terminal and run:  

```bash
git clone --recursive https://github.com/MarvaAI/be-synth-module.git
```

Navigate to the repository folder:  

```bash
cd be-synth-module
```

### *2. Install dependencies*   

```bash
poetry install --with dev
```

### *3. Run the Application*  
To launch the app, run:  

```bash
poetry run streamlit run "app/main.py"
```

### *4. Closing the Application*
To stop the application:

press *Ctrl + C* in the terminal.