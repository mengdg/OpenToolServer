"""open_tool_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from tools import views

urlpatterns = [
    path('project', views.project),
    path('user', views.user),
    path('user/info', views.user_info),
    path('users', views.users),
    path('tool', views.tool),
    path('tools', views.tools),
    path('debugtalk', views.debugtalk),
    path('wisdom', views.wisdom),
    path('logs', views.logs),
    path('visit', views.visit),
    path('viewer', views.viewer),
    path('launch', views.launch),
    path('kind', views.kind),
    path('navigation', views.navigation),
    path('navigations', views.navigations)
]
