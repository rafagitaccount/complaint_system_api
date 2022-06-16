from decouple import config
import boto3


class SESServices:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET_KEY")
        self.region = config("AWS_SES_REGION")
        self.ses = boto3.client("ses",
                    region_name=self.region,
                    aws_access_key_id=self.key,
                    aws_secret_access_key=self.secret
        )


    def send_mail(self, subject, to_addresses, text_data):
        charset = "UTF-8"
        body = {"Text": {"Data": text_data, "Charset": charset}}

        self.ses.send_email(
            Source="pararafaeloliveira@yahoo.com.br",
            Destination={"ToAddresses": to_addresses,
                "CcAddresses": [],
                "BccAddresses": []
            },
            Message={"Subject": {"Data": subject, "Charset": charset},
            "Body": body}
        )
        
