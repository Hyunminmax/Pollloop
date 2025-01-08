from django.urls import path
from .views import (
    FormCreateView, FormListView, FormView, 
    FormInvitedView, FormSubmitView, FromSummaryView, 
    FromDataView, FormCompletedUserView, FormBookmarkView
)

urlpatterns = [
    path('uuid:<slug:uuid>/', FormView.as_view(), name='FormLoad'),
    path('create/', FormCreateView.as_view(), name='NewForm'),
    path('invited/', FormInvitedView.as_view(), name='FormInvited'),
    path('summary/uuid:<slug:uuid>', FromSummaryView.as_view(), name='FormSummary'),
    path('summary/data/uuid:<slug:uuid>', FromDataView.as_view(), name='FormData'),
    path('summary/users/uuid:<slug:uuid>', FormCompletedUserView.as_view(), name='FormCompletedUser'),
    path('submit/', FormSubmitView.as_view(), name='FormSubmit'),
    path('list/user_id:<user_id>/', FormListView.as_view(), name='FormList'),
    path('list/bookmark/', FormBookmarkView.as_view(), name='FormBookmark'),
]
