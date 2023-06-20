package com.codenicely.gimbook.saudi.einvoice.data.di

import EmployeeRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.SplashRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.auth.AuthRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.businessDetailRepo.BusinessDetailRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.creditNoteDebitNote.CreditNoteDebitNoteRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.customerDetailRepo.CustomerDetailRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.historyRepo.HistoryRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.invoiceRepo.InvoiceRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.masterRepo.MasterRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.permissionRepo.PermissionsRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.productRepo.ProductRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.purchaseRepo.PurchaseRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.quotation.QuotationRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.report.ReportRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.setting.SettingRepo
import com.codenicely.gimbook.saudi.einvoice.data.source.subscriptionRepo.SubscriptionRepo
import org.koin.dsl.module
import kotlin.math.sin

/**
 * Use the [repositoryModule] to creating repository instance
 **/
val repositoryModule = module {

    single { SplashRepo(get(), get())}

    single { AuthRepo(get(), get())}

    single { BusinessDetailRepo(get(),get()) }

    factory { MasterRepo(get(),get()) }
    single { CustomerDetailRepo(get(),get()) }
    single { ProductRepo(get(),get()) }
    single { InvoiceRepo(get(),get()) }
    single { CreditNoteDebitNoteRepo(get(),get()) }
    single { PurchaseRepo(get(),get()) }
    single{ SubscriptionRepo(get(),get()) }
    single{ QuotationRepo(get(),get()) }
    single{ SettingRepo(get(),get(),get()) }
    single { ReportRepo(get(),get()) }
    single { HistoryRepo(get(),get()) }
    single { EmployeeRepo(get(), get()) }
    single { PermissionsRepo(get(), get()) }



}