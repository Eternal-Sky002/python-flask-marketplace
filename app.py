from flask import Flask, redirect, url_for
from modules.item.routes import item_bp
from modules.store.routes import store_bp
from modules.transaction.routes import transaction_bp
from modules.user.routes import user_bp

def create_app():
        
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(transaction_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8081, debug=True)