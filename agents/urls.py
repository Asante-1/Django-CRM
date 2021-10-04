from django.urls import path
app_name= 'agents'

from . import views

urlpatterns = [
    path('agent_list/', views.AgentListView.as_view(), name='agent_list_view'),
    path('agent_create/', views.AgentCreateView.as_view(), name='agent_create_view'),
    path('<int:pk>', views.AgentDetailView.as_view(), name='agent_detail_view'),
    path('<int:pk>/update', views.UpdateAgentview.as_view(), name='agent_update_view'),
    path('<int:pk>/delete', views.DeleteView.as_view(), name='agent_delete_view'),

]