def init_app(app):
    """Register all blueprints for the application."""
    
    # Main application routes
    from . import home
    app.register_blueprint(home.bp)

    # Authentication and user-related routes
    from .auths import auth, user_profile, todo, blog, rest_api_book_bp
    app.register_blueprint(auth.bp)
    app.register_blueprint(user_profile.bp)
    app.register_blueprint(todo.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(rest_api_book_bp.bp)

    # Content-specific routes
    from .contents import (
      database_bp, dom_bp, js_bp, home_bp, java_bp, python_bp, spring_bp,
    )
    app.register_blueprint(database_bp.bp)
    app.register_blueprint(dom_bp.bp)
    app.register_blueprint(js_bp.bp)
    app.register_blueprint(home_bp.bp)
    app.register_blueprint(java_bp.bp)
    app.register_blueprint(python_bp.bp)
    app.register_blueprint(spring_bp.bp)
