Check packer version

        packer --version

Packer file validate or not

        packer validate windows.json

Packer build command

        packer build windows.json


environment variables ( Terraform && Packer )

        Linux

            export ARM_TENANT_ID=xxxxxxxxxxxxxxxxxxxxxxxxx
            export ARM_SUBSCRIPTION_ID=xxxx-xxxx-xxxx-xxxx
            export ARM_CLIENT_ID=xxxx-xxxx-xxxx-xxxx
            export ARM_CLIENT_SECRET=xxxx-xxxx-xxxx-xxxx
            
            
        Windows
        
            set ARM_TENANT_ID=xxxxxxxxxxxxxxxxxxxxxxxxx
            set ARM_SUBSCRIPTION_ID=xxxx-xxxx-xxxx-xxxx
            set ARM_CLIENT_ID=xxxx-xxxx-xxxx-xxxx
            set ARM_CLIENT_SECRET=xxxx-xxxx-xxxx-xxxx
        
