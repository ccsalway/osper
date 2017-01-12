import bcrypt
from datetime import timedelta
from flask import Flask, request, render_template, redirect, url_for

from models.cards import *
from models.login import *
from models.user import *
from models.payment import payment


# - initiate flask
app = Flask(__name__)


# - web routes
@app.route('/')
def index():
    return redirect(url_for('do_login'))


# - displays a login form and handles credential checking
@app.route('/login', methods=['GET', 'POST'])
def do_login():
    un = error = ''
    if request.method == 'POST':
        try:
            un = request.form.get('un', '').strip()
            pw = request.form.get('pw')  # do not manipulate input password
            if not un or not pw:
                raise UserWarning('Please enter your email and password')
            user = get_user_by_username(un)
            if not user:
                raise UserWarning("Invalid email or password")
            pswd = user['password'].encode('utf-8')
            if not bcrypt.hashpw(pw.encode('utf-8'), pswd) == pswd:
                raise UserWarning("Invalid email or password")
            access_token = create_access_token(user['userid'])
            response = redirect(url_for("list_cards"))
            response.set_cookie('access_token', access_token)
            return response
        except UserWarning as e:
            error = e.message
    return render_template('login.html', username=un, error=error)


# - displays a list of cards associated to the user's account
@app.route('/cards', methods=['GET'])
def list_cards():
    # check user logged in
    access_token = request.cookies.get('access_token')
    user = check_user_login(access_token)
    if not user:
        return redirect(url_for('do_login'))

    # get cards and render page
    cards = get_cards_by_accountid(user['accid'])
    return render_template('cards.html', cards=cards)


# - displays a payment form and handles top-up
@app.route('/topup', methods=['GET', 'POST'])
def do_topup():
    # check user logged in
    access_token = request.cookies.get('access_token')
    user = check_user_login(access_token)
    if not user:
        return redirect(url_for('do_login'))

    # get card details
    cardid = request.args.get('id')
    card = get_card_by_id(user['accid'], cardid)
    if not card:
        return redirect(url_for('list_cards'))

    # compliance checks
    try:
        available = compliance_checks(card)
    except UserWarning as e:
        return render_template('topup.html', error=e.message, level=0)  # level 0 gives a link back to the cards

    # process top-up payment
    if request.method == 'POST':
        try:
            # - check input
            amount = request.form.get('amount')
            if not amount or not amount.isdigit():  # assume only whole amounts
                raise UserWarning('Missing or invalid amount')
            if int(amount) > available:
                raise UserWarning('Amount exceeds maximum top-up amount of %s' % available)
            nonce = request.form.get('nonce')
            if not nonce:
                raise UserWarning('Missing card token')

            # - process payment
            errors = payment.sale_nonce(nonce, amount)
            if errors:
                raise UserWarning(errors.replace('\n', '<br>'))
            else:
                increase_card_balance(cardid, amount)
                return redirect(url_for('list_cards'))

        except UserWarning as e:
            return render_template('topup.html', error=e.message, level=1, cardid=cardid)  # level 1 gives a link back to the topup

    # display form (GET only)
    client_token = payment.public_auth_token()
    return render_template('topup.html', card=card, available=available, client_token=client_token)


if __name__ == '__main__':
    app.run(debug=True)
