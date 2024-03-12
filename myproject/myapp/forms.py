# forms.py
from django import forms

class InstrumentDetectionForm(forms.Form):
    audio_file = forms.FileField(
        label='Select an audio file',
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
            'id': 'audio_file',
            'name': 'audio_file',
            'accept': '.mp3,.wav',
            'onchange': 'loadAudioFile(event)'
        })
    )

