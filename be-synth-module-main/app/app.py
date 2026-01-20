import streamlit as st
from fractions import Fraction
from shruti import Shruti
from sf2_generator import Sf2Generator
import tkinter as tk
from tkinter import filedialog
import base64, os, shruti, midi


class App:
    default_base_key = midi.get_base_note("C4")
    default_base_freq = 261.626 


    def run(self):
        st.set_page_config(page_title="Sur", page_icon="🎵")
#         st.markdown(
#     "<h3 style='white-space: nowrap;'>"
#     "<img src='' width='50' height='50' style='vertical-align: middle; margin-right: 5px;'>"
#     "Sur - Soundfont Generator</h3>",
#     unsafe_allow_html=True
# )
        st.markdown(
    f"<h3 style='white-space: nowrap;'>"
    f"<img src='data:image/png;base64,{base64.b64encode(open('app/resources/marva1.png', 'rb').read()).decode()}' width='50' height='50' style='vertical-align: middle; margin-right: 10px;'>"
    f"Sur - Soundfont Generator</h3>",
    unsafe_allow_html=True
)


        st.caption("Generate instrument soundfonts based on Western or Hindustani frequency mappings")

        # st.markdown("<h4 style='white-space: nowrap;'> – Western & Indian Notations</h4>", unsafe_allow_html=True)
        selected_option = st.sidebar.selectbox("Select an instrument:", ["Harmonium"])
    
        self.tuning_type = st.sidebar.radio("Tuning Type", ["Western", "Hindustani"])
        self.base_key = self.default_base_key
        self.base_freq = self.default_base_freq

        self.setup_base_key_input()
        self.setup_base_freq_input()
        self.setup_generate_button()

        is_disabled = self.tuning_type == "Western"  # Disable table for Western tuning

        self.setup_shruti_table(is_disabled)

    def setup_base_key_input(self):
        midi_input = st.sidebar.text_input("Enter Key with Octave", value=self.default_base_key)

        try:
            self.base_midi = midi.note_to_midi(midi_input)
            base_key = midi_input
            st.sidebar.text(f"Base Key: {midi.midi_to_note(self.base_midi)}")
            self.base_key = midi.get_base_note(base_key)

        except:
            st.sidebar.error("Invalid Key Input")


    def setup_base_freq_input(self):
        base_freq_input = st.sidebar.text_input("Base Frequency (Hz)", value=str(self.default_base_freq))
        self.base_freq = self.validate_freq(base_freq_input)

        if not self.base_freq:
            st.sidebar.error("Please enter a valid frequency.")


    def setup_generate_button(self):
        if st.sidebar.button("Generate Soundfont"):

            dir = self.ask_directory()

            if not dir:
                st.sidebar.error("Select folder to generate soundfont file")

            try:
                if self.tuning_type == "Hindustani":
                    ratios = self.get_selected_ratios()
                    generator = Sf2Generator(base_midi=self.base_midi, base_freq=self.base_freq, ratios=ratios)
                else:
                    generator = Sf2Generator(base_midi=self.base_midi, base_freq=self.base_freq)

                file_path = os.path.join(dir, "Harmonium.sf2")
                generator.write(file_path)
                st.sidebar.success("Soundfont generated successfully!")
            except:
                st.sidebar.error("Soundfont generation failed.")


    def ask_directory(self) -> str:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.attributes('-topmost', True)
            root.update()
            dir = filedialog.askdirectory(title="Select a Folder")
            root.destroy()

            return dir


    def get_selected_ratios(self) -> tuple[float]:
        ratios = []

        for note in midi.notes:
            freq_ratio_key = f"{note}_freq_ratio"
            selected_freq_ratio = st.session_state.get(freq_ratio_key, None)

            if not selected_freq_ratio:
                st.error("Ratio column parse error.")
            
            try:
                ratios.append(float(Fraction(selected_freq_ratio)))
            except ValueError:
                st.error(f"Invalid frequency ratio: {selected_freq_ratio}")
        
        return tuple(ratios)
        

    @staticmethod
    def validate_freq(freq: float):
        min_freq = 16.0
        max_freq = 20000.0

        try:
            freq = float(freq)
        except:
            return None

        if not (min_freq <= freq <= max_freq):
            return None
        
        return freq


    def get_note_sequence(self, base_note: str) -> tuple[str]:
        notes = midi.notes

        if base_note not in notes:
            st.error(f"Base Key {base_note} is not valid. Please choose a valid key.")
            return None

        # Shift the keys to start from the base key
        base_note_index = notes.index(base_note)

        return tuple(notes[base_note_index:] + notes[:base_note_index])
    
    
    def setup_shruti_table(self, is_disabled: bool):
        # Create faded effect if disabled
        fade_style = "opacity: 0.4;" if is_disabled else ""
        table_style = "text-align: center;"
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 2, 2])  # Adjust column widths

        with col1:
            st.markdown(f'<div style="{fade_style}"><b>Key</b></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="{fade_style}"><b>Swara</b></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="{fade_style}"><b>Shruti</b></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div style="{fade_style}"><b>Symbol</b></div>', unsafe_allow_html=True)
        with col5:
            st.markdown(f'<div style="{fade_style}"><b>Ratio</b></div>', unsafe_allow_html=True)

        notes = self.get_note_sequence(self.base_key)
        shrutis = shruti.default_shrutis
        selected_ratios = []

        # Table Rows         
        for note, shruti_enum in zip(notes, shrutis):
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 2, 2])

            with col1:
                st.markdown(f'<div style="{fade_style}"><b>{note}</b></div>', unsafe_allow_html=True)

            swara_name = shruti.names[shruti_enum]['swara']
            with col2:
                st.markdown(f'<div style="{fade_style}">{swara_name}</div>', unsafe_allow_html=True)

            symbol_options = [x.value for x in shruti.get_pair_tuple(shruti_enum)]

            for default_index in range(len(symbol_options)):
                if Shruti(symbol_options[default_index]) in shruti.default_shrutis:
                    break

            with col4:
                selected_symbol = st.radio(
                    "", symbol_options, index=default_index, key=f"{note}_symbol", horizontal=True
                )

            selected_shruti_enum = Shruti(selected_symbol)
            shruti_name = shruti.names[selected_shruti_enum]['shruti']
            with col3:
                st.markdown(f'<div style="{fade_style}">{shruti_name}</div>', unsafe_allow_html=True)

            freq_ratio = shruti.freq_multipliers[selected_shruti_enum]
            with col5:
                selected_freq_ratio = st.text_input("", value=str(Fraction(freq_ratio).limit_denominator()), key=f"{note}_freq_ratio", disabled=is_disabled)

            selected_ratios.append(selected_freq_ratio)

        return tuple(selected_ratios)
