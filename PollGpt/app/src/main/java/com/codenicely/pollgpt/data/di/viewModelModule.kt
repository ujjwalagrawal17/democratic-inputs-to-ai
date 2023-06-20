package com.codenicely.gimbook.saudi.einvoice.data.di


import com.codenicely.gimbook.saudi.einvoice.model.permissionModel.PermissionsListModel
import com.codenicely.gimbook.saudi.einvoice.ui.auth.views.mobileVerification.viewmodel.MobileVerificationViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.auth.views.otpFragment.viewmodel.OtpVerificationViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.auth.views.setupProfile.ViewModel.SetupProfileViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.viewmodel.MasterViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.bankDetails.viewmodel.BankDetailViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.createInvoice.viewmodel.InvoiceViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.creditDebitNoteList.viewmodel.CreditDebitNoteViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.customerDetail.viewmodel.CustomerDetailViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.customerList.viewmodel.CustomerListViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.debitCreditnote.viewmodel.DebitCreditNoteViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.editBusinessDetail.viewModel.BusinessDetailViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.employeeCreateFragment.viewModels.PermissionViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.employeeListFragment.viewModels.EmployeeListViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.history.historyViewModel.HistoryViewModel
import com.codenicely.gimbook.saudi.einvoice.model.setting.homeFragment.homeViewModel.HomeViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.invoiceListFragment.viewmodel.InvoiceListViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.paymentReceipt.CreatePaymentReceipt.viewmodel.CreatePaymentReceiptModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.productFragment.viewmodel.ProductViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.productList.viewModel.ProductListViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.purchase.viewmodel.PurchaseViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.purchaseList.viewModel.PurchaseListViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.quotation.viewmodel.QuotationViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.quotationList.viewmodel.QuotationListViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.report.partyWise.viewModel.PartyWiseViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.report.partyWiseDetailFragment.viewModel.PartyWiseDetailViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.report.partyWiseDetailFragment.viewModel.ProductDetailViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.report.productWise.ProductViewModel.ProductWiseViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.setting.invoiceTemplate.viewmodel.TemplateViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.setting.whatsAppDocumentList.viewmodel.DocumentListViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.subscription.viewModel.SubscriptionViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.maindashboard.views.subscriptionHistory.viewmodel.SubscriptionHistoryViewModel
import com.codenicely.gimbook.saudi.einvoice.ui.splash.viewmodel.SplashViewModel

import org.koin.android.viewmodel.dsl.viewModel
import org.koin.dsl.module

/**
 * Use the [viewModelModule] to creating viewModel instance
 **/
val viewModelModule = module {



    viewModel { MasterViewModel(get()) }
    viewModel { SplashViewModel(get()) }
    viewModel { MobileVerificationViewModel(get()) }
    viewModel { OtpVerificationViewModel(get()) }
    viewModel { SetupProfileViewModel(get()) }
    viewModel { BusinessDetailViewModel(get()) }
    viewModel { BankDetailViewModel(get()) }
    viewModel { CustomerDetailViewModel(get()) }
    viewModel { CustomerListViewModel(get()) }
    viewModel { ProductViewModel(get()) }
    viewModel { ProductListViewModel(get()) }
    viewModel { InvoiceViewModel(get()) }
    viewModel { InvoiceListViewModel(get()) }
    viewModel { CreditDebitNoteViewModel(get()) }
    viewModel { DebitCreditNoteViewModel(get()) }
    viewModel { PurchaseViewModel(get()) }
    viewModel { PurchaseListViewModel(get()) }
    viewModel { SubscriptionViewModel(get()) }
    viewModel { SubscriptionHistoryViewModel(get()) }
    viewModel { QuotationViewModel(get()) }
    viewModel { QuotationListViewModel(get()) }
    viewModel { DocumentListViewModel(get()) }
    viewModel { PartyWiseViewModel(get()) }
    viewModel { PartyWiseDetailViewModel(get()) }
    viewModel { ProductWiseViewModel(get()) }
    viewModel { ProductDetailViewModel(get()) }
    viewModel { CreatePaymentReceiptModel(get()) }
    viewModel { TemplateViewModel(get()) }
    viewModel { HomeViewModel(get()) }
    viewModel { HistoryViewModel(get()) }
    viewModel { EmployeeListViewModel(get()) }
    viewModel { PermissionViewModel(get()) }











}