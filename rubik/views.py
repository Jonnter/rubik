from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from users.models import UserProfile

# Create your views here.


class IndexViews(LoginRequiredMixin,TemplateView):
    template_name = "index.html"


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super(IndexViews, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get_user_count():
        return UserProfile.objects.count()

    def get_context_data(self, **kwargs):
        # week_ago = timezone.now() - timezone.timedelta(weeks=1)
        # month_ago = timezone.now() - timezone.timedelta(days=30)
        # self.session_week = Session.objects.filter(date_start__gt=week_ago)
        # self.session_month = Session.objects.filter(date_start__gt=month_ago)
        # self.session_month_dates = self.session_month.dates('date_start', 'day')
        #
        # self.session_month_dates_archive = []
        # time_min = datetime.datetime.min.time()
        # time_max = datetime.datetime.max.time()
        #
        # for d in self.session_month_dates:
        #     ds = datetime.datetime.combine(d, time_min).replace(
        #         tzinfo=timezone.get_current_timezone())
        #     de = datetime.datetime.combine(d, time_max).replace(
        #         tzinfo=timezone.get_current_timezone())
        #     self.session_month_dates_archive.append(
        #         self.session_month.filter(date_start__range=(ds, de)))

        context = {
            # 'assets_count': self.get_asset_count(),
            'users_count': self.get_user_count(),
            # 'online_user_count': self.get_online_user_count(),
            # 'online_asset_count': self.get_online_session_count(),
            # 'user_visit_count_weekly': self.get_week_login_user_count(),
            # 'asset_visit_count_weekly': self.get_week_login_asset_count(),
            # 'user_visit_count_top_five': self.get_top5_user_a_week(),
            # 'month_str': self.get_month_day_metrics(),
            # 'month_total_visit_count': self.get_month_login_metrics(),
            # 'month_user': self.get_month_active_user_metrics(),
            # 'mouth_asset': self.get_month_active_asset_metrics(),
            # 'month_user_active': self.get_month_active_user_total(),
            # 'month_user_inactive': self.get_month_inactive_user_total(),
            # 'month_user_disabled': self.get_user_disabled_total(),
            # 'month_asset_active': self.get_month_active_asset_total(),
            # 'month_asset_inactive': self.get_month_inactive_asset_total(),
            # 'month_asset_disabled': self.get_asset_disabled_total(),
            # 'week_asset_hot_ten': self.get_week_top10_asset(),
            # 'last_login_ten': self.get_last10_sessions(),
            # 'week_user_hot_ten': self.get_week_top10_user(),
            # 'app': _("Dashboard"),
        }

        kwargs.update(context)
        return super(IndexViews, self).get_context_data(**kwargs)

def page_not_found(request):
    return render(request, 'error.html')

def server_error(request):
    return render(request, 'error.html')

def permission_denied(request):
    return render(request, 'error.html')



class ErrorPageViews(TemplateView):
    template_name = "error.html"


