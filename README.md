# ML-Voice

Real-time voice, in a form suitable for machine learning.  
<br>


## Requirement

Linux
```
sudo apt install portaudio19-dev
```

MacOS
```
brew install portaudio
```
<br>


## Installation

```
pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade poetry
poetry install
```
<details>
<summary>When an error occurs on Linux</summary>

```
sudo apt install git gcc make zlib1g-dev libffi-dev libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev python3-tk python3-distutils python3-pip
```
</details>
<details>
<summary>When an error occurs on Windows</summary>

- If you get an error when installing simpleaudio
    1. Install or update [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/ja/visual-cpp-build-tools/)
    1. Reboot the computer
</details>
<br>


## Usage

Linux or MacOS    
```
poetry run python recording_example.py
```

Windows 10 or 11
```
poetry run python.exe recording_example.py
```
<br>


## Note

- [x] Load from wav
- [x] Load from microphone  
<br>


## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.  
<br>


### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.


### Redistribution

<details>
<summary>PyAudio</summary>

[MIT License](https://people.csail.mit.edu/hubert/pyaudio/)
```
├── lib
│   ├── LICENSE
│   ├── PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
│   ├── PyAudio-0.2.11-cp38-cp38-win_amd64.whl
│   └── PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```
</details>