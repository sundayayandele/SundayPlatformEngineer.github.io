Excellent — here's how to add a pre-validation step in your pipeline that:

✅ Verifies the private key is:

Present

In -----BEGIN PRIVATE KEY----- format (i.e., unencrypted / nocrypt)


🚫 Fails the pipeline early if:

The key is missing or

It is encrypted (-----BEGIN ENCRYPTED PRIVATE KEY-----)



---

✅ Add This Pre-Validation Step (after fetching the key)

In your templates/pfx-job.yml, update the Setup step to include this logic after saving the private key:

- task: AzureCLI@2
  name: Setup
  displayName: 'Convert CRT to PEM and Fetch Private Key'
  inputs:
    azureSubscription: ${{ parameters.azureServiceConnection }}
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      echo "Copying full-chain .crt to PEM..."
      cp "${{ parameters.crtFilePath }}" cert.pem

      echo "Retrieving private key from Key Vault..."
      az keyvault secret show \
        --vault-name ${{ parameters.keyVaultName }} \
        --name ${{ parameters.privateKeySecretName }} \
        --query value -o tsv | sed 's/\r//' > private.key

      echo "Validating private key format..."
      first_line=$(head -n 1 private.key)

      if [ "$first_line" == "-----BEGIN ENCRYPTED PRIVATE KEY-----" ]; then
        echo "❌ ERROR: The private key is encrypted. Please provide an unencrypted (nocrypt) private key."
        exit 1
      fi

      if [ "$first_line" != "-----BEGIN PRIVATE KEY-----" ]; then
        echo "❌ ERROR: The private key format is invalid or corrupted. Found: $first_line"
        exit 1
      fi

      echo "✅ Private key format is valid (nocrypt)."


---

🔐 What This Step Does:

Fetches the key from Key Vault

Strips Windows newlines (\r)

Checks if the key is encrypted or invalid

Fails early with a clear error message



---

🚫 Example Failure Message

If the key is encrypted:

❌ ERROR: The private key is encrypted. Please provide an unencrypted (nocrypt) private key.

If it's malformed:

❌ ERROR: The private key format is invalid or corrupted. Found: -----BEGIN RSA PRIVATE KEY-----


---

Would you like to also fail if the certificate itself is already expired or expires too soon (e.g., < 30 days)?

