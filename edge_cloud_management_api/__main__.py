from edge_cloud_management_api.app import get_app_instance

if __name__ == "__main__":
    app = get_app_instance()
    app.run(host="0.0.0.0", port=8080)
