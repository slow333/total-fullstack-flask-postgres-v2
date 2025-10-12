from .routes.auths import auth, blog, rest_api_book_bp, todo, user_profile
from .routes.contents import contents_bp, database_bp, home_bp, spring_bp

def init_app(app):
    """Register all blueprints for the application."""
    
    # Authentication and user-related blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(rest_api_book_bp.bp)
    app.register_blueprint(todo.bp)
    app.register_blueprint(user_profile.bp)

    # Content and documentation blueprints
    app.register_blueprint(contents_bp.bp)
    app.register_blueprint(database_bp.bp)
    app.register_blueprint(home_bp.bp)
    app.register_blueprint(spring_bp.bp)
