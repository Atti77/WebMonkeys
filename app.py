from flask import Flask, request, jsonify, render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
recipient_email = os.getenv('RECIPIENT_EMAIL')

app = Flask(__name__,
            template_folder='templates',  # Módosított útvonal
            static_folder='static'        # Módosított útvonal
        )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-contact', methods=['POST'])
def send_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        html_content = f"""
        <html>
            <body>
                <h2>Új kapcsolatfelvételi űrlap érkezett</h2>
                <table style="border-collapse: collapse; width: 100%;">
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Név:</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>E-mail:</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{email}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Telefonszám:</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{phone}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Üzenet:</strong></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{message}</td>
                    </tr>
                </table>
            </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Új kapcsolatfelvétel - {name}"
        msg.attach(MIMEText(html_content, 'html'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            return jsonify({"success": True, "message": "Üzenet sikeresen elküldve!"})
        except Exception as e:
            return jsonify({"success": False, "message": f"Hiba történt: {str(e)}"})

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)