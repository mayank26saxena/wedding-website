import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config.from_object(Config)

# Set up Google Sheets client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(app.config['CREDENTIALS_FILE'], scope)
client = gspread.authorize(creds)

# Open the specific sheets
guest_list_sheet = client.open(app.config['SPREADSHEET_NAME']).worksheet(app.config['GUEST_LIST_SHEET_NAME'])
rsvp_sheet = client.open(app.config['SPREADSHEET_NAME']).worksheet(app.config['RSVP_SHEET_NAME'])

@app.route('/')
def home():
    wedding_date = datetime(2024, 11, 21)
    today = datetime.today()
    days_to_go = (wedding_date - today).days
    return render_template('home.html', days_to_go=days_to_go)

@app.route('/our_story')
def our_story():
    return render_template('our_story.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/travel')
def travel():
    return render_template('travel.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        secret_code = request.form['secret_code'].strip()

        # Verify against Google Sheet
        guest_list = guest_list_sheet.get_all_records()
        print(guest_list)
        guest = next((guest for guest in guest_list if guest['First Name'].strip().lower() == first_name.lower() and guest['Last Name'].strip().lower() == last_name.lower() and guest['Secret Code'] == secret_code), None)

        if guest:
            session['authenticated'] = True
            session['first_name'] = first_name
            session['last_name'] = last_name
            return redirect(url_for('rsvp_form'))
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('auth.html')

@app.route('/rsvp/form', methods=['GET', 'POST'])
def rsvp_form():
    if not session.get('authenticated'):
        return redirect(url_for('rsvp'))

    if request.method == 'POST':
        attendance = request.form['attendance']
        first_name = session['first_name']
        last_name = session['last_name']

        # Fetch the RSVP records
        rsvp_records = rsvp_sheet.get_all_records()
        updated = False

        for i, record in enumerate(rsvp_records, start=2):  # Starting from row 2
            if record['First Name'].strip().lower() == first_name.lower() and record['Last Name'].strip().lower() == last_name.lower():
                # Update the existing record
                rsvp_sheet.update_cell(i, list(record.keys()).index('Attendance') + 1, attendance)
                updated = True
                break

        if not updated:
            # Append a new record if no existing record is found
            rsvp_sheet.append_row([first_name, last_name, attendance])

        return redirect(url_for('thank_you'))

    return render_template('rsvp_form.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
