from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from config import api_call

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    return redirect(url_for('user.dashboard'))

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Debug: Print the data being sent
        login_data = {
            'username': username,
            'password': password
        }
        # print(f"Attempting login with data: {login_data}")
        
        response = api_call('POST', '/login', login_data)
        
        # Debug: Print response details
        # if response:
        #     print(f"Response status: {response.status_code}")
        #     print(f"Response content: {response.text}")
        # else:
        #     print("No response received from API")
        
        if response and response.status_code == 200:
            data = response.json()
            # print("Login response data:", data)  # Debug print
            
            session['user_id'] = data.get('user_id')
            session['username'] = username
            session['access_token'] = data.get('access_token')
            session['role'] = data.get('role')
            
            # print("Session after login:", dict(session))  # Debug print
            
            flash('Login berhasil!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            error_message = 'Username atau password salah!'
            if response:
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        error_message = error_data['message']
                except:
                    pass
            flash(error_message, 'error')
    
    return render_template('user/login.html')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Debug: Print the data being sent
        register_data = {
            'username': username,
            'password': password,
            'role': 'ROLE_ADMIN'
        }
        # print(f"Attempting registration with data: {register_data}")
        
        response = api_call('POST', '/register', register_data)
        
        # Debug: Print response details
        # if response:
        #     print(f"Response status: {response.status_code}")
        #     print(f"Response content: {response.text}")
        # else:
        #     print("No response received from API")
        
        if response and response.status_code == 201:
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('user.login'))
        else:
            error_message = 'Registrasi gagal! Username mungkin sudah ada.'
            if response:
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        error_message = error_data['message']
                except:
                    pass
            flash(error_message, 'error')
    
    return render_template('user/register.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('user.login'))

@user_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    # Get items, stores, and tags for dashboard
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    
    items_response = api_call('GET', '/items', headers=headers)
    if items_response and items_response.status_code == 401:
        flash('Sesi Anda telah habis, silakan login ulang.', 'error')
        return redirect(url_for('user.login'))
    stores_response = api_call('GET', '/stores', headers=headers)
    if stores_response and stores_response.status_code == 401:
        flash('Sesi Anda telah habis, silakan login ulang.', 'error')
        return redirect(url_for('user.login'))
    
    items = items_response.json() if items_response else []
    stores = stores_response.json() if stores_response else []
    
    # Process items to extract store names from nested store object
    for item in items:
        if item.get('store') and isinstance(item['store'], dict):
            item['store_name'] = item['store'].get('name', 'Unknown Store')
        else:
            item['store_name'] = 'No Store'
    
    # Get all unique tags from all stores
    all_tags = []
    unique_tag_names = set()
    
    for store in stores:
        store_tags_response = api_call('GET', f'/stores/{store["id"]}/tag', headers=headers)
        if store_tags_response and store_tags_response.status_code == 401:
            flash('Sesi Anda telah habis, silakan login ulang.', 'error')
            return redirect(url_for('user.login'))
        if store_tags_response:
            store_tags = store_tags_response.json()
            for tag in store_tags:
                if tag.get('name') not in unique_tag_names:
                    unique_tag_names.add(tag.get('name'))
                    all_tags.append(tag)
    
    return render_template('user/dashboard.html', 
        items=items, 
        stores=stores, 
        tags=all_tags,
        username=session.get('username'))