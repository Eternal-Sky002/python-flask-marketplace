from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from config import API_BASE_URL

store_bp = Blueprint('store', __name__)

@store_bp.route('/stores/<int:store_id>')
def view_store(store_id):
    response = requests.get(f"{API_BASE_URL}/stores/{store_id}")
    if response.status_code == 200:
        store = response.json()
        return render_template('store/detail.html', store=store)
    flash('Store not found', 'error')
    return redirect(url_for('item.list_items'))
