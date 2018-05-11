from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from django_pesapal.views import PaymentRequestMixin

from .forms import PaymentForm
from .models import Purchase


class PaymentView(PaymentRequestMixin):

    def get_pesapal_payment_iframe(self, order_info):
        '''
        Authenticates with pesapal to get the payment iframe src
        '''
        iframe_src_url = self.get_payment_url(**order_info)
        return iframe_src_url
        
        
class LipaNaMpesaView(TemplateView):
 
    template_name = 'purchase/lipa_mpesa.html'
    
    def get_context_data(self, **kwargs):
        context = super(LipaNaMpesaView, self).get_context_data(**kwargs)        
        
        data = {
                 'first_name': self.request.user.first_name, 
                 'last_name': self.request.user.last_name,
                 'amount': 1000,
                 'description': 'Payment for Workstry Training',
                 'email': self.request.user.email,
                 'reference': self.request.user.id
               }
        form = PaymentForm(initial=data)
        #form = PaymentForm(self.request.POST or None)  # instance= None
        context["form"] = form
        return context
    
    
def process_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST) # A form bound to the POST data
        print(request.POST)
        if form.is_valid(): # All validation rules pass
            paymentview = PaymentView()
            paymentview.request = request
            payment_url = paymentview.get_pesapal_payment_iframe(form.cleaned_data)
            return HttpResponseRedirect(payment_url) # Redirect after POST
        else:
            print(form.errors)    
            
    else:
        data = {
                 'first_name': request.user.first_name, 
                 'last_name': request.user.last_name,
                 'amount': 1000,
                 'description': 'Payment for Workstry Training',
                 'email': request.user.email,
                 'reference': request.user.id
               }
        form = PaymentForm(initial=data)
    return render(request, 'purchase/lipa_mpesa.html', {
        'form': form,
    })
    
    
def process_payment_feedback(request):
    # TODO: Get payment status and process
    """tx = request.REQUEST['tx']
    result = pesapal.Verify( tx )
    if result.success() and resource.price == result.amount(): # valid
      purchase = models.Purchase( resource=resource, purchaser=user, tx=tx )
      purchase.save()
      return render_to_response('purchased.html', { 'resource': resource }, ..."""
  
  
     
    pesapal_merchant_reference = request.GET['pesapal_merchant_reference']
    pesapal_transaction_tracking_id = request.GET['pesapal_transaction_tracking_id']
    purchase = Purchase( purchaser=request.user, pesapal_tx_id=pesapal_transaction_tracking_id )
    purchase.save()
    return render(request, 'purchase/payment_feedback.html', {})
