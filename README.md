# [Ransomware Sample In Python That Encrypt and Decrypt Files]
To run this:
- `pip3 install -r requirements.txt`
- 
    ```
    python crypt --help
    ```
    **Output:**
    ```
    usage: losgeld.py [-h]

    optional arguments:
    -h, --help          show this help message and exit
    --keyfile           Path to keyfile
    ```
- If you want to encrypt
    ```
    python losgeld.py --action encrypt
    ```
- To decrypt it ('Path to keyfile must be specified after --keyfile for decryption'):
    ```
    python losgeld.py --action decrypt --keyfile ./path/to/keyfile
    ```
