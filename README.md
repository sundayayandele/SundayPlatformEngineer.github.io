# SundayPlatformEngineer.github.io

Here is the complete, production-ready Azure DevOps pipeline setup tailored for your .crt full-chain file (with 3 certificates) stored in the repo.


---

📁 Folder Structure Assumed:

.
├── azure-pipelines.yml
├── templates/
│   └── pfx-job.yml
└── certs/
    └── certificate-chain.crt  # full chain: leaf + intermediates + root


---

✅ azure-pipelines.yml (Main Pipeline)

trigger:
- main

parameters:
  - name: crtFilePath
    type: string
    default: 'certs/certificate-chain.crt'  # full-chain .crt file in repo

variables:
  keyVaultName: 'YOUR_KEYVAULT_NAME'
  azureServiceConnection: 'YOUR_AZURE_SERVICE_CONNECTION'
  privateKeySecretName: 'private-key'
  pfxOutputFile: 'output.pfx'
  pfxPasswordSecretName: 'pfx-password'
  pfxSecretName: 'pfx-bundle'
  checksumSecretName: 'pfx-checksum'

stages:
- stage: GenerateAndUploadPfx
  displayName: 'Convert Full Chain CRT to Encrypted PFX'
  jobs:
  - template: templates/pfx-job.yml
    parameters:
      crtFilePath: ${{ parameters.crtFilePath }}
      keyVaultName: $(keyVaultName)
      azureServiceConnection: $(azureServiceConnection)
      privateKeySecretName: $(privateKeySecretName)
      pfxOutputFile: $(pfxOutputFile)
      pfxPasswordSecretName: $(pfxPasswordSecretName)
      pfxSecretName: $(pfxSecretName)
      checksumSecretName: $(checksumSecretName)


---

✅ templates/pfx-job.yml (Reusable Job Template)

parameters:
  crtFilePath: ''
  keyVaultName: ''
  azureServiceConnection: ''
  privateKeySecretName: ''
  pfxOutputFile: ''
  pfxPasswordSecretName: ''
  pfxSecretName: ''
  checksumSecretName: ''

jobs:
- job: ConvertAndUpload
  displayName: 'Convert Full-Chain CRT to Encrypted PFX and Upload'
  pool:
    vmImage: 'ubuntu-latest'
  steps:

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
        privateKey=$(az keyvault secret show --vault-name ${{ parameters.keyVaultName }} --name ${{ parameters.privateKeySecretName }} --query value -o tsv)
        echo "$privateKey" > private.key

  - script: |
      echo "Generating random password for PFX..."
      pfxPassword=$(openssl rand -base64 24)
      echo "$pfxPassword" > pfx_password.txt

      echo "Generating encrypted .pfx from full-chain PEM and private key..."
      openssl pkcs12 -export \
        -inkey private.key \
        -in cert.pem \
        -out ${{ parameters.pfxOutputFile }} \
        -passout pass:$pfxPassword \
        -name "CertWithFullChain"

      echo "Computing SHA256 checksum for .pfx..."
      sha256sum ${{ parameters.pfxOutputFile }} | awk '{print $1}' > pfx_checksum.txt
    displayName: 'Generate Encrypted .pfx and Checksum'

  - task: AzureCLI@2
    displayName: 'Upload PFX, Password, and Checksum to Key Vault'
    inputs:
      azureSubscription: ${{ parameters.azureServiceConnection }}
      scriptType: 'bash'
      scriptLocation: 'inlineScript'
      inlineScript: |
        echo "Uploading PFX password..."
        az keyvault secret set --vault-name ${{ parameters.keyVaultName }} --name ${{ parameters.pfxPasswordSecretName }} --value "$(cat pfx_password.txt)"

        echo "Uploading encrypted PFX file..."
        az keyvault secret set --vault-name ${{ parameters.keyVaultName }} --name ${{ parameters.pfxSecretName }} --file ${{ parameters.pfxOutputFile }}

        echo "Uploading checksum..."
        az keyvault secret set --vault-name ${{ parameters.keyVaultName }} --name ${{ parameters.checksumSecretName }} --value "$(cat pfx_checksum.txt)"

        echo "Secure cleanup of temporary files..."
        shred -u private.key pfx_password.txt pfx_checksum.txt cert.pem


---

✅ Summary of Outputs Stored in Azure Key Vault:

Secret Name	Content

pfx-password	Random password for PFX encryption
pfx-bundle	The .pfx file (encrypted)
pfx-checksum	SHA256 checksum of the PFX



---

