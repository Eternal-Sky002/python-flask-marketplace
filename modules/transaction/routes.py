from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from config import api_call, API_BASE_URL
from datetime import datetime

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions')
def list_transactions():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    user_id = session.get('user_id')
    response = api_call('GET', f'/transactions/user/{user_id}', headers=headers)

    if response.status_code == 200:
        transactions = response.json()
        return render_template('transaction/list.html', transactions=transactions)
    flash('Error fetching transactions', 'error')
    return render_template('transaction/list.html', transactions=[])

@transaction_bp.route('/transactions/<int:transaction_id>')
def view_transaction(transaction_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    response = api_call('GET', f'/transactions/{transaction_id}', headers=headers)
    if response.status_code == 200:
        transaction = response.json()
        # Convert string timestamp to datetime object
        if transaction.get('transaction_time'):
            try:
                transaction['transaction_time'] = datetime.fromisoformat(transaction['transaction_time'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                transaction['transaction_time'] = None
        return render_template('transaction/detail.html', transaction=transaction)
    flash('Transaction not found', 'error')
    return redirect(url_for('transaction.list_transactions'))

@transaction_bp.route('/transactions/create', methods=['GET', 'POST'])
def create_transaction():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('user.login'))
    
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    
    # Get item_id from either URL params (GET) or form data (POST)
    item_id = request.args.get('item_id') if request.method == 'GET' else request.form.get('item_id')
    if request.method == 'POST':
        # Convert form data to appropriate types
        try:
            qty = int(request.form.get('qty', 1))
            user_id = int(session.get('user_id'))
            # Get item_id from form data instead of URL parameter
            form_item_id = request.form.get('item_id')
            # print(f'form_item_id: {form_item_id}')
            
            if not form_item_id:
                flash('Item ID tidak valid', 'error')
                return redirect(url_for('item.list_items'))
                
            item_id = int(form_item_id)
            # print(f'try: {item_id}')
            
            if not item_id:
                flash('Item ID tidak valid', 'error')
                return redirect(url_for('item.list_items'))
            
            transaction_data = {
                'user_id': user_id,
                'item_id': item_id,
                'qty': qty
            }
            
            # print("Sending transaction data:", transaction_data)  # Debug print
            
            response = api_call('POST', '/transactions', transaction_data, headers=headers)
            # print("Response:", response.status_code, response.text)  # Debug print
            
            if response.status_code == 201:
                flash('Transaksi berhasil dibuat', 'success')
                return redirect(url_for('transaction.list_transactions'))
            elif response.status_code == 422:
                error_msg = response.json().get('message', 'Data tidak valid')
                flash(f'Error: {error_msg}', 'error')
            else:
                flash('Error saat membuat transaksi', 'error')
        except ValueError:
            flash('Data yang dimasukkan tidak valid', 'error')
            
    # GET request - show form
    item = None
    if item_id:
        item_response = api_call('GET', f'/items/{item_id}', headers=headers)
        if item_response and item_response.status_code == 401:
            flash('Sesi Anda telah habis, silakan login ulang.', 'error')
            return redirect(url_for('user.login'))
        elif item_response and item_response.status_code == 200:
            item = item_response.json()
        else:
            flash('Item tidak ditemukan', 'error')
            return redirect(url_for('item.list_items'))

    return render_template('transaction/create.html', item_id=item_id, item=item)

@transaction_bp.route('/transactions/<int:transaction_id>/update-status', methods=['POST'])
def update_transaction_status(transaction_id):
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('user.login'))

    status = request.form.get('status')
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    
    response = api_call('PUT', f'/transactions/payment/{transaction_id}/{status}', headers=headers)
    if response and response.status_code == 200 or 201:
        status_messages = {
            '2': 'Pembayaran berhasil',
            '3': 'Transaksi dibatalkan'
        }
        flash(status_messages.get(status, 'Status transaksi berhasil diupdate'), 'success')
    else:
        error_msg = response.json().get('message', 'Error updating transaction status') if response else 'Error updating transaction status'
        flash(error_msg, 'error')
    return redirect(url_for('transaction.view_transaction', transaction_id=transaction_id))
