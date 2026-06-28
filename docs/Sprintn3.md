**Ciclo 4**

**SMART MOBILITY**

Versione 3.0

Data di rilascio: 28/06/2026

Ingegneria del Software a. A. 2025-2026\
**Informatica e Tecnologie per la Produzione del Software**

**Realizzato da**

Cardone Flavio 829469 ITPS

[f.cardone21@studenti.uniba.it](https://unibari-my.sharepoint.com/personal/f_cardone21_studenti_uniba_it/Documents/f.cardone21@studenti.uniba.it)

De Astis Gabriele 826243 ITPS

g.deastis1@studenti.uniba.it

Giannulo Francesco 825071 ITPS

<f.giannulo@studenti.uniba.it>

Lacirignola Camilla 830465 ITPS

<c.lacirignola5@studenti.uniba.it>

Indice

[1. Product Backlog [8](#product-backlog)](#product-backlog)

[1.1 Introduzione [8](#introduzione)](#introduzione)

[1.2 Contesto di business [9](#contesto-di-business)](#contesto-di-business)

[1.3 Stakeholder [10](#stakeholder)](#stakeholder)

[1.4 Item funzionali [11](#item-funzionali)](#item-funzionali)

[1.4.1 IF-UT.01 – Visualizza Mappa Utente [11](#if-ut.01-visualizza-mappa-utente)](#if-ut.01-visualizza-mappa-utente)

[1.4.2 IF-UT.02 – Prenota mezzo [11](#if-ut.02-prenota-mezzo)](#if-ut.02-prenota-mezzo)

[1.4.4 IF-UT.03 – Sblocca mezzo [11](#if-ut.03-sblocca-mezzo)](#if-ut.03-sblocca-mezzo)

[1.4.5 IF-UT.04 – Termina Corsa [12](#if-ut.04-termina-corsa)](#if-ut.04-termina-corsa)

[1.4.6 IF-UT.05 – Effettua Pagamento [12](#if-ut.05-effettua-pagamento)](#if-ut.05-effettua-pagamento)

[1.4.7 IF-UT.06 – Salva Metodi Pagamento [12](#if-ut.06-salva-metodi-pagamento)](#if-ut.06-salva-metodi-pagamento)

[1.4.8 IF-UT.07 – Consulta tariffe [12](#if-ut.07-consulta-tariffe)](#if-ut.07-consulta-tariffe)

[1.4.9 IF-UT.08 – Visualizza Riepilogo corsa [12](#if-ut.08-visualizza-riepilogo-corsa)](#if-ut.08-visualizza-riepilogo-corsa)

[1.4.10 IF-UT.09 – Sospende Corsa [12](#if-ut.09-sospende-corsa)](#if-ut.09-sospende-corsa)

[1.4.11 IF-UT.10 – Visualizza Promozioni [13](#if-ut.10-visualizza-promozioni)](#if-ut.10-visualizza-promozioni)

[1.4.12 IF-UT.11 – Visualizza Storico Corsa [13](#if-ut.11-visualizza-storico-corsa)](#if-ut.11-visualizza-storico-corsa)

[1.4.13 IF-UT.12 – Invia Segnalazione [13](#if-ut.12-invia-segnalazione)](#if-ut.12-invia-segnalazione)

[1.4.14 IF-UT.13 – Sottoscrive Abbonamento [13](#if-ut.13-sottoscrive-abbonamento)](#if-ut.13-sottoscrive-abbonamento)

[1.4.15 IF-UT.14 – Visualizza Suggerimenti Intelligenti [13](#if-ut.14-visualizza-suggerimenti-intelligenti)](#if-ut.14-visualizza-suggerimenti-intelligenti)

[1.4.16 IF-UT.15 – Scrive una recensione [13](#if-ut.15-scrive-una-recensione)](#if-ut.15-scrive-una-recensione)

[1.4.17 IF-AP.01 – Accede Report [14](#if-ap.01-accede-report)](#if-ap.01-accede-report)

[1.4.18 IF-AP.02 – Esporta Report [14](#if-ap.02-esporta-report)](#if-ap.02-esporta-report)

[1.4.19 IF-AP.03 – Visualizza Mappa Amministrazione Pubblica [14](#if-ap.03-visualizza-mappa-amministrazione-pubblica)](#if-ap.03-visualizza-mappa-amministrazione-pubblica)

[1.4.20 IF-OP.01 – Visualizza Mappa Operatore [14](#if-op.01-visualizza-mappa-operatore)](#if-op.01-visualizza-mappa-operatore)

[1.4.21 IF-OP.02 – Aggiunge Mezzo [14](#if-op.02-aggiunge-mezzo)](#if-op.02-aggiunge-mezzo)

[1.4.22 IF-OP.03 – Dismette Mezzo [14](#if-op.03-dismette-mezzo)](#if-op.03-dismette-mezzo)

[1.4.23 IF-OP.04 – Modifica Stato Mezzo [15](#if-op.04-modifica-stato-mezzo)](#if-op.04-modifica-stato-mezzo)

[1.4.24 IF-OP.05 – Definisce Tariffa [15](#if-op.05-definisce-tariffa)](#if-op.05-definisce-tariffa)

[1.4.25 IF-OP.06 – Definisce Regole Fine Corsa [15](#if-op.06-definisce-regole-fine-corsa)](#if-op.06-definisce-regole-fine-corsa)

[1.4.26 IF-OP.07 - Definisce Zona [15](#if-op.07---definisce-zona)](#if-op.07---definisce-zona)

[1.4.27 IF-OP.08 – Gestisce Segnalazioni [15](#if-op.08-gestisce-segnalazioni)](#if-op.08-gestisce-segnalazioni)

[1.4.28 IF-OP.09 – Sospende Account Utente [15](#if-op.09-sospende-account-utente)](#if-op.09-sospende-account-utente)

[1.4.29 IF-OP.10– Definisce Offerte [16](#if-op.10-definisce-offerte)](#if-op.10-definisce-offerte)

[1.4.30 IF-OP.11 – Configura Parametri Numerici di Sistema [16](#if-op.11-configura-parametri-numerici-di-sistema)](#if-op.11-configura-parametri-numerici-di-sistema)

[1.4.31 IF-OP.12 – Visualizza Recensioni [16](#if-op.12-visualizza-recensioni)](#if-op.12-visualizza-recensioni)

[1.4.32 IF-OP.13 – Mostra Storico Modifiche [16](#if-op.13-mostra-storico-modifiche)](#if-op.13-mostra-storico-modifiche)

[1.5 Item non funzionali [16](#item-non-funzionali)](#item-non-funzionali)

[1.5.1 Item Informativi [16](#item-informativi)](#item-informativi)

[1.5.1.1 IIN-1 Prestazioni [16](#iin-1-prestazioni)](#iin-1-prestazioni)

[1.5.1.2 IIN-2 Sicurezza [17](#iin-2-sicurezza)](#iin-2-sicurezza)

[1.5.1.3 IIN-3 Usabilità [17](#iin-3-usabilità)](#iin-3-usabilità)

[1.5.1.4 IIN-4 Scalabilità [17](#iin-4-scalabilità)](#iin-4-scalabilità)

[1.5.1.5 IIN-5 Portabilità [17](#iin-5-portabilità)](#iin-5-portabilità)

[1.5.1.6 Conformità [17](#conformità)](#conformità)

[1.5.2 Item di interfaccia [18](#item-di-interfaccia)](#item-di-interfaccia)

[1.5.2.1 IUI-1 - Schermata di Login Utente [18](#iui-1---schermata-di-login-utente)](#iui-1---schermata-di-login-utente)

[1.5.2.2 IUI-2 – Homepage Utente [18](#map-screenshot-showing-a-section-of-bari-italy-with-colored-markers-indicating-different-transportation-options-around-politecnico-di-bari-and-università-degli-studi-di-bari.-blue-markers-represent-bicycles-green-markers-indicate-scooters-and-purple-markers-show-cars-with-a-red-shaded-area-highlighting-politecnico-di-bari-and-a-red-location-pin-marking-a-specific-point-nearby.iui-2-homepage-utente)](#map-screenshot-showing-a-section-of-bari-italy-with-colored-markers-indicating-different-transportation-options-around-politecnico-di-bari-and-università-degli-studi-di-bari.-blue-markers-represent-bicycles-green-markers-indicate-scooters-and-purple-markers-show-cars-with-a-red-shaded-area-highlighting-politecnico-di-bari-and-a-red-location-pin-marking-a-specific-point-nearby.iui-2-homepage-utente)

[1.5.2.3 IUI-3 – Menu Laterale Utente [19](#screenshot-of-a-mobile-app-menu-for-a-smart-mobility-service-displaying-options-in-italian-such-as-profile-pricing-plan-bonuses-and-promotions-history-settings-wallet-and-guide-with-corresponding-icons.-the-menu-overlays-a-partial-map-showing-bike-icons-near-via-giuseppe-re-indicating-bike-sharing-locations.iui-3-menu-laterale-utente)](#screenshot-of-a-mobile-app-menu-for-a-smart-mobility-service-displaying-options-in-italian-such-as-profile-pricing-plan-bonuses-and-promotions-history-settings-wallet-and-guide-with-corresponding-icons.-the-menu-overlays-a-partial-map-showing-bike-icons-near-via-giuseppe-re-indicating-bike-sharing-locations.iui-3-menu-laterale-utente)

[1.5.2.4 IUI-4 – Corsa di Gruppo [19](#iui-4-corsa-di-gruppo)](#iui-4-corsa-di-gruppo)

[1.5.2.5 IUI-5 – Prenotazione Mezzo [20](#screenshot-of-a-scooter-rental-app-interface-showing-a-map-with-a-green-location-pin-indicating-scooter-availability-near-politecnico-di-bari.-the-booking-panel-displays-scooter-id-bz234vf-a-full-battery-icon-and-a-countdown-timer-until-1647-to-unlock-the-scooter-with-a-green-prenota-button-for-reservation.iui-5-prenotazione-mezzo)](#screenshot-of-a-scooter-rental-app-interface-showing-a-map-with-a-green-location-pin-indicating-scooter-availability-near-politecnico-di-bari.-the-booking-panel-displays-scooter-id-bz234vf-a-full-battery-icon-and-a-countdown-timer-until-1647-to-unlock-the-scooter-with-a-green-prenota-button-for-reservation.iui-5-prenotazione-mezzo)

[1.5.2.6 IUI-6 – Visualizzazione del Piano Tariffario [20](#screenshot-of-a-tariff-pricing-chart-for-different-transportation-modes-showing-costs-per-kilometer-for-electric-scooter-0.20km-bicycle-0.30km-and-automobile-0.50km.-the-chart-uses-black-icons-for-each-vehicle-type-alongside-green-text-for-labels-and-prices-with-a-smart-mobility-logo-below-and-navigation-icons-at-the-bottom.iui-6-visualizzazione-del-piano-tariffario)](#screenshot-of-a-tariff-pricing-chart-for-different-transportation-modes-showing-costs-per-kilometer-for-electric-scooter-0.20km-bicycle-0.30km-and-automobile-0.50km.-the-chart-uses-black-icons-for-each-vehicle-type-alongside-green-text-for-labels-and-prices-with-a-smart-mobility-logo-below-and-navigation-icons-at-the-bottom.iui-6-visualizzazione-del-piano-tariffario)

[1.5.2.7 IUI-7 – Visualizzazione del Saldo e Metodi di Pagamento [20](#screenshot-of-a-digital-wallet-interface-showing-a-zero-balance-with-payment-method-options-including-google-pay-apple-pay-paypal-and-credit-card-addition.-the-layout-features-green-text-and-buttons-with-icons-for-each-payment-method-and-a-prominent-green-button-labeled-ricarica-saldo-for-recharging-balance.iui-7-visualizzazione-del-saldo-e-metodi-di-pagamento)](#screenshot-of-a-digital-wallet-interface-showing-a-zero-balance-with-payment-method-options-including-google-pay-apple-pay-paypal-and-credit-card-addition.-the-layout-features-green-text-and-buttons-with-icons-for-each-payment-method-and-a-prominent-green-button-labeled-ricarica-saldo-for-recharging-balance.iui-7-visualizzazione-del-saldo-e-metodi-di-pagamento)

[1.5.2.8 IUI-8 – Schermata Info Corsa [21](#screenshot-of-a-scooter-rental-app-interface-displaying-trip-information.-it-shows-scooter-id-bz234vf-remaining-battery-level-elapsed-time-of-46-seconds-and-distance-traveled-of-0.3-kilometers-with-buttons-to-end-and-pay-or-pause-the-ride.iui-8-schermata-info-corsa)](#screenshot-of-a-scooter-rental-app-interface-displaying-trip-information.-it-shows-scooter-id-bz234vf-remaining-battery-level-elapsed-time-of-46-seconds-and-distance-traveled-of-0.3-kilometers-with-buttons-to-end-and-pay-or-pause-the-ride.iui-8-schermata-info-corsa)

[1.5.2.9 IUI-9 – Visualizzazione della Cronologia Corse [21](#screenshot-of-a-transportation-log-displaying-four-entries-with-icons-for-electric-scooter-bicycle-car-and-another-electric-scooter.-each-entry-includes-id-bz345tr-elapsed-time-1021-distance-traveled-4.98-km-and-date-04052026-with-teal-text-and-icons-on-a-white-background.iui-9-visualizzazione-della-cronologia-corse)](#screenshot-of-a-transportation-log-displaying-four-entries-with-icons-for-electric-scooter-bicycle-car-and-another-electric-scooter.-each-entry-includes-id-bz345tr-elapsed-time-1021-distance-traveled-4.98-km-and-date-04052026-with-teal-text-and-icons-on-a-white-background.iui-9-visualizzazione-della-cronologia-corse)

[1.5.2.10 IUI-10 – Schermata Login Operatore/Amministrazione Pubblica [22](#iui-10-schermata-login-operatoreamministrazione-pubblica)](#iui-10-schermata-login-operatoreamministrazione-pubblica)

[1.5.2.11 IUI-11 – Dashboard Amministrazione Pubblica [22](#iui-11-dashboard-amministrazione-pubblica)](#iui-11-dashboard-amministrazione-pubblica)

[1.5.2.12 IUI-12 – Definizione Zone Vietate [22](#map-showing-a-restricted-zone-in-bari-outlined-by-red-points-indicating-areas-where-certain-vehicles-cannot-enter.-the-right-panel-lists-vehicle-types-with-a-green-checkmark-on-automobile-highlighting-that-cars-are-prohibited-from-the-red-zone-while-scooters-and-bicycles-are-not-restricted.iui-12-definizione-zone-vietate)](#map-showing-a-restricted-zone-in-bari-outlined-by-red-points-indicating-areas-where-certain-vehicles-cannot-enter.-the-right-panel-lists-vehicle-types-with-a-green-checkmark-on-automobile-highlighting-that-cars-are-prohibited-from-the-red-zone-while-scooters-and-bicycles-are-not-restricted.iui-12-definizione-zone-vietate)

[1.5.2.13 IUI-13 – Definizione Zone Limitate [23](#iui-13-definizione-zone-limitate)](#iui-13-definizione-zone-limitate)

[1.5.2.14 IUI-14 – Definizione Zone di Parcheggio [23](#iui-14-definizione-zone-di-parcheggio)](#iui-14-definizione-zone-di-parcheggio)

[1.5.2.15 IUI-15 – Visualizzazione dei Report [24](#bar-chart-and-pie-chart-displaying-weekly-and-overall-distribution-of-three-categories-monopattini-green-automobili-pink-and-biciclette-blue.-bar-chart-shows-daily-counts-with-monopattini-highest-on-monday-and-decreasing-through-the-week-while-pie-chart-highlights-monopattini-as-majority-at-55.8-followed-by-biciclette-at-31.3-and-automobili-at-11.4.iui-15-visualizzazione-dei-report)](#bar-chart-and-pie-chart-displaying-weekly-and-overall-distribution-of-three-categories-monopattini-green-automobili-pink-and-biciclette-blue.-bar-chart-shows-daily-counts-with-monopattini-highest-on-monday-and-decreasing-through-the-week-while-pie-chart-highlights-monopattini-as-majority-at-55.8-followed-by-biciclette-at-31.3-and-automobili-at-11.4.iui-15-visualizzazione-dei-report)

[1.5.2.16 IUI-16 – Dashboard Operatore [24](#iui-16-dashboard-operatore)](#iui-16-dashboard-operatore)

[1.5.2.17 IUI-17 – Gestione Segnalazioni [24](#iui-17-gestione-segnalazioni)](#iui-17-gestione-segnalazioni)

[1.5.2.18 IUI-18 – Gestione Tariffe e Promozioni [25](#iui-18-gestione-tariffe-e-promozioni)](#iui-18-gestione-tariffe-e-promozioni)

[1.5.2.19 IUI-19 – Schermata di Impostazione Regole [25](#screenshot-of-a-settings-panel-titled-impostazioni-regole-displaying-configurable-rules-for-booking-and-business-operations.-it-includes-fields-with-numerical-values-for-maximum-booking-duration-30-min-grace-period-for-pause-10-min-maximum-concurrent-bookings-per-user-5-tariff-percentage-during-pause-100-and-a-dropdown-menu-with-options-related-to-business-rules-outside-parking-zones.iui-19-schermata-di-impostazione-regole)](#screenshot-of-a-settings-panel-titled-impostazioni-regole-displaying-configurable-rules-for-booking-and-business-operations.-it-includes-fields-with-numerical-values-for-maximum-booking-duration-30-min-grace-period-for-pause-10-min-maximum-concurrent-bookings-per-user-5-tariff-percentage-during-pause-100-and-a-dropdown-menu-with-options-related-to-business-rules-outside-parking-zones.iui-19-schermata-di-impostazione-regole)

[2. Sprint Report [27](#sprint-report)](#sprint-report)

[2.1 Sprint Backlog [27](#sprint-backlog)](#sprint-backlog)

[2.2 Product Requirement Specification [29](#product-requirement-specification)](#product-requirement-specification)

[2.2.1 Diagramma dei Casi d’uso [29](#diagramma-dei-casi-duso)](#diagramma-dei-casi-duso)

[2.2.2 Specifiche dei Casi d’uso [30](#specifiche-dei-casi-duso)](#specifiche-dei-casi-duso)

[2.2.2.1 UT – 01 Visualizza Mappa Utente [30](#ut-01-visualizza-mappa-utente)](#ut-01-visualizza-mappa-utente)

[2.2.2.2 UT – 02 Prenota Mezzo [32](#ut-02-prenota-mezzo)](#ut-02-prenota-mezzo)

[2.2.2.3 UT – 03 Sblocca Mezzo [34](#ut-03-sblocca-mezzo)](#ut-03-sblocca-mezzo)

[2.2.2.4 UT – 04 Termina corsa [36](#ut-04-termina-corsa)](#ut-04-termina-corsa)

[2.2.2.5 UT – 05 Effettua Pagamento [38](#ut-05-effettua-pagamento)](#ut-05-effettua-pagamento)

[2.2.2.6 UT - 06 Salva Metodo di Pagamento [40](#ut---06-salva-metodo-di-pagamento)](#ut---06-salva-metodo-di-pagamento)

[2.2.2.1 UT – 07 Consulta Tariffe [42](#ut-07-consulta-tariffe)](#ut-07-consulta-tariffe)

[2.2.2.2 UT – 08 Visualizza Riepilogo Corsa [44](#ut-08-visualizza-riepilogo-corsa)](#ut-08-visualizza-riepilogo-corsa)

[2.2.2.3 UT – 09 Sospende Corsa [44](#ut-09-sospende-corsa)](#ut-09-sospende-corsa)

[2.2.2.4 UT – 10 Visualizza Promozioni [46](#ut-10-visualizza-promozioni)](#ut-10-visualizza-promozioni)

[2.2.2.5 UT – 11 Visualizza Storico Corse [48](#ut-11-visualizza-storico-corse)](#ut-11-visualizza-storico-corse)

[2.2.2.6 UT – 12 Invia Segnalazione [49](#ut-12-invia-segnalazione)](#ut-12-invia-segnalazione)

[2.2.2.7 UT – 13 Sottoscrive Abbonamento [50](#ut-13-sottoscrive-abbonamento)](#ut-13-sottoscrive-abbonamento)

[2.2.2.8 UT – 14 Visualizza Suggerimenti Intelligenti [51](#ut-14-visualizza-suggerimenti-intelligenti)](#ut-14-visualizza-suggerimenti-intelligenti)

[2.2.2.9 UT – 15 Scrive Recensione [53](#ut-15-scrive-recensione)](#ut-15-scrive-recensione)

[2.2.2.10 AP – 01 Accede Report [55](#ap-01-accede-report)](#ap-01-accede-report)

[2.2.2.11 AP - 02 Esporta Report [56](#ap---02-esporta-report)](#ap---02-esporta-report)

[2.2.2.12 AP – 03 Visualizza Mappa Amministrazione Pubblica [58](#ap-03-visualizza-mappa-amministrazione-pubblica)](#ap-03-visualizza-mappa-amministrazione-pubblica)

[2.2.2.13 OP – 01 Visualizza Mappa Operatore [60](#op-01-visualizza-mappa-operatore)](#op-01-visualizza-mappa-operatore)

[2.2.2.14 OP – 02 Aggiunge Mezzo [61](#op-02-aggiunge-mezzo)](#op-02-aggiunge-mezzo)

[2.2.2.15 OP – 03 Dismette Mezzo [63](#op-03-dismette-mezzo)](#op-03-dismette-mezzo)

[2.2.2.16 OP – 04 Modifica stato mezzo [65](#op-04-modifica-stato-mezzo)](#op-04-modifica-stato-mezzo)

[2.2.2.17 OP – 05 Definisce tariffa [66](#op-05-definisce-tariffa)](#op-05-definisce-tariffa)

[2.2.2.18 OP-06 Definisce Regole Fine Corsa [68](#op-06-definisce-regole-fine-corsa)](#op-06-definisce-regole-fine-corsa)

[2.2.2.19 OP-07 Definisce Zona [69](#op-07-definisce-zona)](#op-07-definisce-zona)

[2.2.2.20 OP-08 Gestisce Segnalazione [70](#op-08-gestisce-segnalazione)](#op-08-gestisce-segnalazione)

[2.2.2.21 OP-09 Sospende Account Utente [71](#op-09-sospende-account-utente)](#op-09-sospende-account-utente)

[2.2.2.22 OP-10 Definisce Offerta [73](#op-10-definisce-offerta)](#op-10-definisce-offerta)

[2.2.2.23 OP-11 Configura parametri numerici di sistema [74](#op-11-configura-parametri-numerici-di-sistema)](#op-11-configura-parametri-numerici-di-sistema)

[2.2.2.24 OP-12 Visualizza Recensioni [75](#op-12-visualizza-recensioni)](#op-12-visualizza-recensioni)

[2.2.2.25 OP-13 Mostra storico modifiche [77](#op-13-mostra-storico-modifiche)](#op-13-mostra-storico-modifiche)

[2.3 System Architecture [78](#system-architecture)](#system-architecture)

[2.3.1 Diagramma delle Componenti – Diagramma Generale [78](#diagramma-delle-componenti-diagramma-generale)](#diagramma-delle-componenti-diagramma-generale)

[2.3.1.1 Client [79](#client)](#client)

[2.3.1.2 Server [79](#server)](#server)

[2.3.2 Specifica delle componenti [79](#specifica-delle-componenti)](#specifica-delle-componenti)

[Specifica delle componenti client [80](#specifica-delle-componenti-client)](#specifica-delle-componenti-client)

[2.3.2.1 Specifica delle componenti server [80](#specifica-delle-componenti-server)](#specifica-delle-componenti-server)

[2.3.2.2 Specifica delle componenti Servizi Esterni [81](#specifica-delle-componenti-servizi-esterni)](#specifica-delle-componenti-servizi-esterni)

[2.3.2.3 Specifica delle interfacce e del flusso di comunicazione [81](#specifica-delle-interfacce-e-del-flusso-di-comunicazione)](#specifica-delle-interfacce-e-del-flusso-di-comunicazione)

[2.4 Detailed Product Design [82](#detailed-product-design)](#detailed-product-design)

[2.4.1 Diagramma delle Classi – Diagramma Generale [82](#diagramma-delle-classi-diagramma-generale)](#diagramma-delle-classi-diagramma-generale)

[2.4.1.1 Diagramma delle Classi – Client [82](#diagramma-delle-classi-client)](#diagramma-delle-classi-client)

[2.4.1.2 Diagramma delle Classi – Server [83](#diagramma-delle-classi-server)](#diagramma-delle-classi-server)

[2.4.1.3 Diagramma delle Classi – View [83](#diagramma-delle-classi-view)](#diagramma-delle-classi-view)

[2.4.1.4 Diagramma delle Classi – APIService [83](#diagramma-delle-classi-apiservice)](#diagramma-delle-classi-apiservice)

[2.4.1.5 Diagramma delle Classi – Controller [83](#diagramma-delle-classi-controller)](#diagramma-delle-classi-controller)

[2.4.1.6 Diagramma delle Classi – Business Logic Layer [84](#diagramma-delle-classi-business-logic-layer)](#diagramma-delle-classi-business-logic-layer)

[2.4.1.7 Diagramma delle Classi – Data Access Layer [84](#diagramma-delle-classi-data-access-layer)](#diagramma-delle-classi-data-access-layer)

[2.4.1.8 Diagramma delle Classi – Model [84](#diagramma-delle-classi-model)](#diagramma-delle-classi-model)

[2.4.1.9 Diagramma delle Classi – Servizi Esterni [85](#diagramma-delle-classi-servizi-esterni)](#diagramma-delle-classi-servizi-esterni)

[2.4.2 Specifiche delle Classi [86](#specifiche-delle-classi)](#specifiche-delle-classi)

[2.4.2.1 Specifica delle Classi – Client [86](#specifica-delle-classi-client)](#specifica-delle-classi-client)

[2.4.2.1.1 View — Presentation Layer [86](#view-presentation-layer)](#view-presentation-layer)

[2.4.2.1.2 API Service [89](#api-service)](#api-service)

[2.4.2.2 Specifica delle Classi – Server [91](#specifica-delle-classi-server)](#specifica-delle-classi-server)

[2.4.2.2.1 Controller [91](#controller)](#controller)

[2.4.2.2.2 BLL – Business Logic Layer [92](#bll-business-logic-layer)](#bll-business-logic-layer)

[2.4.2.2.3 DAL – Data Acces Layer [94](#dal-data-acces-layer)](#dal-data-acces-layer)

[2.4.2.2.4 Model [96](#model)](#model)

[2.4.2.3 Interfacce e comunicazione tra componenti [98](#interfacce-e-comunicazione-tra-componenti)](#interfacce-e-comunicazione-tra-componenti)

[2.4.2.3.1 Client → Server: API Service → Controller [98](#client-server-api-service-controller)](#client-server-api-service-controller)

[2.4.2.3.2 Controller → BLL: [98](#controller-bll)](#controller-bll)

[2.4.2.3.3 BLL →DAL: [99](#bll-dal)](#bll-dal)

[2.4.2.3.4 Model: [99](#model-1)](#model-1)

[2.4.2.3.5 Integrazione con i sistemi esterni: [99](#integrazione-con-i-sistemi-esterni)](#integrazione-con-i-sistemi-esterni)

[2.4.2.3.6 DBMS: [100](#dbms)](#dbms)

[2.4.3 Diagrammi di Sequenza [101](#diagrammi-di-sequenza)](#diagrammi-di-sequenza)

[2.4.3.1 UT - 01 Visualizza Mappa Utente [101](#ut---01-visualizza-mappa-utente)](#ut---01-visualizza-mappa-utente)

[2.4.3.2 UT - 02 Prenota Mezzo [102](#ut---02-prenota-mezzo)](#ut---02-prenota-mezzo)

[2.4.3.3 UT – 03 Sblocca Mezzo [103](#ut-03-sblocca-mezzo-1)](#ut-03-sblocca-mezzo-1)

[2.4.3.4 UT – 04 Termina Corsa [104](#ut-04-termina-corsa-1)](#ut-04-termina-corsa-1)

[2.4.3.5 UT – 05 Effettua Pagamento [105](#ut-05-effettua-pagamento-1)](#ut-05-effettua-pagamento-1)

[2.4.3.6 UT – 06 Salva Metodo di Pagamento [106](#ut-06-salva-metodo-di-pagamento)](#ut-06-salva-metodo-di-pagamento)

[2.4.3.7 UT – 07 Consulta Tariffe [108](#ut-07-consulta-tariffe-1)](#ut-07-consulta-tariffe-1)

[2.4.3.8 UT – 08 Visualizza Riepilogo Corsa [108](#ut-08-visualizza-riepilogo-corsa-1)](#ut-08-visualizza-riepilogo-corsa-1)

[2.4.3.9 UT - 09 Sospende Corsa [109](#ut---09-sospende-corsa)](#ut---09-sospende-corsa)

[2.4.3.10 UT – 10 Visualizza Promozioni [110](#ut-10-visualizza-promozioni-1)](#ut-10-visualizza-promozioni-1)

[2.4.3.11 UT – 11 Visualizza Storico Corse [111](#ut-11-visualizza-storico-corse-1)](#ut-11-visualizza-storico-corse-1)

[2.4.3.12 UT – 12 Invia Segnalazione [112](#ut-12-invia-segnalazione-1)](#ut-12-invia-segnalazione-1)

[2.4.3.13 UT – 13 Sottoscrive Abbonamento [113](#ut-13-sottoscrive-abbonamento-1)](#ut-13-sottoscrive-abbonamento-1)

[2.4.3.14 UT – 14 Visualizza Suggerimenti Intelligenti [114](#ut-14-visualizza-suggerimenti-intelligenti-1)](#ut-14-visualizza-suggerimenti-intelligenti-1)

[2.4.3.15 UT – 15 Scrive Recensione [115](#ut-15-scrive-recensione-1)](#ut-15-scrive-recensione-1)

[2.4.3.16 AP – 01 Accede Report [116](#ap-01-accede-report-1)](#ap-01-accede-report-1)

[2.4.3.17 AP – 02 Esporta Report [116](#ap-02-esporta-report)](#ap-02-esporta-report)

[2.4.3.18 AP – 03 Visualizza Mappa Amministrazione Pubblica [117](#ap-03-visualizza-mappa-amministrazione-pubblica-1)](#ap-03-visualizza-mappa-amministrazione-pubblica-1)

[2.4.3.19 OP-01 Visualizza Mappa Operatore [117](#op-01-visualizza-mappa-operatore-1)](#op-01-visualizza-mappa-operatore-1)

[2.4.3.20 OP – 02 Aggiunge Mezzo [118](#op-02-aggiunge-mezzo-1)](#op-02-aggiunge-mezzo-1)

[2.4.3.21 OP – 03 Dismette Mezzo [119](#op-03-dismette-mezzo-1)](#op-03-dismette-mezzo-1)

[2.4.3.22 OP – 04 Modifica Stato Mezzo [120](#op-04-modifica-stato-mezzo-1)](#op-04-modifica-stato-mezzo-1)

[2.4.3.23 OP – 05 Definisce Tariffa [121](#op-05-definisce-tariffa-1)](#op-05-definisce-tariffa-1)

[2.4.3.24 OP – 06 Definisce Regole fine corsa [122](#op-06-definisce-regole-fine-corsa-1)](#op-06-definisce-regole-fine-corsa-1)

[2.4.3.25 OP – 07 Definisce Zona [123](#op-07-definisce-zona-1)](#op-07-definisce-zona-1)

[2.4.3.26 OP – 08 Gestisce Segnalazione [124](#op-08-gestisce-segnalazione-1)](#op-08-gestisce-segnalazione-1)

[2.4.3.27 OP – 09 Sospende account utente [125](#op-09-sospende-account-utente-1)](#op-09-sospende-account-utente-1)

[2.4.3.28 OP – 10 Definisce Offerta [126](#op-10-definisce-offerta-1)](#op-10-definisce-offerta-1)

[2.4.3.29 OP – 11 Configura Parametri Numerici Sistema [127](#op-11-configura-parametri-numerici-sistema)](#op-11-configura-parametri-numerici-sistema)

[2.4.3.30 OP – 12 Visualizza Recensioni [128](#op-12-visualizza-recensioni-1)](#op-12-visualizza-recensioni-1)

[2.4.3.31 OP – 13 Mostra Storico Modifiche [128](#op-13-mostra-storico-modifiche-1)](#op-13-mostra-storico-modifiche-1)

[2.5 Data modeling and design [129](#data-modeling-and-design)](#data-modeling-and-design)

[2.5.1 Modello logico del Database [129](#modello-logico-del-database)](#modello-logico-del-database)

[2.5.2 Struttura fisica del Database [130](#struttura-fisica-del-database)](#struttura-fisica-del-database)

[Prompt [131](#prompt)](#prompt)

[2.6 Qualità dei requisiti [131](#qualità-dei-requisiti)](#qualità-dei-requisiti)

[2.7 Diagrammi UML [138](#diagrammi-uml)](#diagrammi-uml)

[2.7.1 Diagramma delle componenti [138](#diagramma-delle-componenti)](#diagramma-delle-componenti)

[2.7.2 Diagramma delle classi [139](#diagramma-delle-classi)](#diagramma-delle-classi)

[2.7.3 Diagrammi di Sequenza [141](#diagrammi-di-sequenza-1)](#diagrammi-di-sequenza-1)

[2.7.4 Codifica [141](#codifica)](#codifica)

[3. Glossario [145](#glossario)](#glossario)

[3.1 Acronimi [145](#acronimi)](#acronimi)

[3.2 Definizioni [145](#definizioni)](#definizioni)

Product Backlog

**CICLO 4**

**SMART MOBILITY**

# Product Backlog

## Introduzione 

**SMART MOBILITY** è un sistema software progettato per supportare l'introduzione di un servizio integrato di mobilità urbana sostenibile, che mette a fattor comune diversi servizi di sharing (bike sharing, car sharing, e-scooter sharing) in un'unica piattaforma accessibile a cittadini, operatori e amministrazione pubblica.

Il Sistema si pone tre obiettivi macroscopici:

- Offrire ai cittadini un accesso rapido, sicuro e trasparente ai mezzi di sharing disponibili sul territorio

- Permettere agli Operatori del Servizio di gestire in modo efficiente la flotta, riducendo costi operativi e fenomeni di vandalismo

- Consentire all'Amministrazione Pubblica di monitorare la mobilità urbana e supportare la pianificazione territoriale con dati aggregati

Tali obiettivi si traducono in un insieme di funzionalità che coprono l'intero ciclo di utilizzo del servizio, rispondendo alle esigenze delle tre categorie di utenti destinatari del sistema: Utenti, Operatori del Servizio e Amministrazione Pubblica.

Per gli **Utenti**, SMART MOBILITY offre:

- Visualizzazione dei mezzi disponibili nelle vicinanze e del loro stato

- Prenotazione di uno o più mezzi e sblocco tramite dispositivo personale

- Pagamenti veloci e sicuri, con meccanismi di prevenzione di frodi ed errori

- Promozioni, abbonamenti, pausa della corsa e gestione del profilo di pagamento

Per gli **Operatori del Servizio**, SMART MOBILITY offre:

- Visualizzazione della distribuzione della flotta sul territorio per ottimizzare il riposizionamento dei mezzi

- Monitoraggio di malfunzionamenti, pianificazione della manutenzione e tracciamento della posizione dei mezzi a fine corsa, per contenere furti e vandalismo

- Bonus per parcheggio corretto, sospensione dell'account in caso di frode.

- Definizione di Zone Vietate, Zone Limitate, Zone di Parcheggio e del confine operativo della flotta

Per l'Amministrazione Pubblica, SMART MOBILITY offre:

- Monitoraggio della frequenza di utilizzo delle diverse tipologie di mezzo, con ripartizione per giorno della settimana e per tipologia

- Accesso a report aggregati settimanali (corse totali, durata media, distanza totale), esportabili in formato CSV e PDF, a supporto della pianificazione strategica

- Monitoraggio dello stato della flotta (mezzi disponibili, in uso, in manutenzione) per una visione d'insieme dell'operatività del servizio

- Visualizzazione cartografica del territorio operativo, con vista a pin, cluster o heatmap dei mezzi e delle zone, per il monitoraggio complessivo del servizio

## Contesto di business

Nel panorama urbano contemporaneo — segnato dall'emergenza climatica, dalla necessità di decongestionare i centri storici e dalla transizione verso modelli di "Smart City" — emerge con forza l'esigenza di soluzioni integrate per la mobilità condivisa.

SMART Mobility nasce per rispondere a questa esigenza, superando la frammentazione degli attuali servizi di sharing e offrendo una piattaforma unica che connette cittadini, operatori privati e pubblica amministrazione.

Il software è pensato per i seguenti ambiti applicativi:

- **Mobilità dei cittadini.** In un contesto urbano dove possedere un mezzo privato è sempre più costoso e inefficiente, i cittadini necessitano di strumenti che permettano di pianificare spostamenti intermodali in tempo reale. SMART Mobility offre un ecosistema che permette di localizzare, prenotare e pagare diversi tipi di mezzo (biciclette, monopattini, auto elettriche) tramite un'unica interfaccia, con piena trasparenza su tariffe e disponibilità e con incentivi (bonus) per comportamenti corretti, come il parcheggio nelle aree designate.

- **Gestione operativa della flotta.** La gestione di una flotta di mezzi condivisi comporta sfide logistiche significative: dal recupero dei mezzi scarichi alla manutenzione dopo atti vandalici. Gli Operatori del Servizio necessitano di strumenti per il monitoraggio costante della flotta, la gestione delle zone operative e l'ottimizzazione del riposizionamento dei mezzi. SMART Mobility fornisce una dashboard che consente di definire Zone Vietate, Zone Limitate, Zone di Parcheggio e il confine operativo, regolando in tempo reale la circolazione sul territorio e riducendo i costi di recupero.

- **Governance dell'Amministrazione Pubblica**. I comuni si trovano spesso a subire la proliferazione di servizi di sharing senza disporre di strumenti adeguati per monitorarli. SMART Mobility offre una dashboard che consente di osservare in tempo reale la distribuzione dei mezzi e lo stato della flotta sul territorio (mezzi disponibili, in uso, in manutenzione), con vista a pin, cluster o heatmap, e rendendo disponibili report aggregati settimanali, esportabili in CSV e PDF, a supporto della pianificazione strategica della mobilità urbana.

> In questo scenario, SMART Mobility si propone come piattaforma integrata che supera i limiti dei singoli servizi proprietari, offrendo un'esperienza fluida e centralizzata alle esigenze di tutti gli attori della mobilità urbana.

## Stakeholder

Il sistema SMART Mobility coinvolge diversi stakeholder che interagiscono con la piattaforma con ruoli e obiettivi specifici:

**1. Utente** È l'utente che usufruisce dei mezzi di mobilità condivisa. Deve essere registrato per visualizzare la mappa, localizzare i mezzi, prenotarli e pagarli. Le tipologie di Utente sono:

- *Pendolare Urbano*: utilizza regolarmente il servizio per coprire l'ultimo miglio (es. da stazione a ufficio) e cerca affidabilità e abbonamenti convenienti.

- *Utente Occasionale*: residente che utilizza il servizio saltuariamente, per necessità impreviste o svago.

- *Turista*: visitatore che necessita di un accesso rapido e senza frizioni per esplorare la città in modo sostenibile.

**2. Operatore del Servizio** Rappresenta l'azienda che immette i mezzi sul territorio e ne gestisce il business e la manutenzione. Le figure interne all'Operatore sono:

- *Manager del Servizio*: definisce piani tariffari, promozioni, zone operative e zone soggette a restrizione, per massimizzare il profitto e regolare la circolazione dei mezzi.

- *Team Logistico e Manutentori*: personale sul campo che si occupa della ricarica delle batterie, della riparazione dei guasti e del riposizionamento fisico dei mezzi nelle zone ad alta richiesta.

**3. Amministrazione Pubblica** Ente che supervisione l’utilizzo dei mezzi nel suolo pubblico. La figura coinvolta è:

- *Pianificatore Urbano / Mobility Manager*: utilizza i dati e i report aggregati della piattaforma per analizzare i flussi di mobilità, studiare nuovi percorsi ciclabili e supportare le decisioni di pianificazione urbana.

## Item funzionali

Contiene l’elenco e la specifica di tutti i requisiti funzionali espressi attraverso lo schema delle user stories:

### IF-UT.01 – Visualizza Mappa Utente

*Come* utente,

*Voglio* visualizzare la “Mappa Utente”,

*Così da* poter scegliere un mezzo.

### IF-UT.02 – Prenota mezzo

*Come* utente,

*Voglio* prenotare uno o più mezzi disponibili,

*Così da* trovarli riservati al mio arrivo.

### 1.4.4 IF-UT.03 – Sblocca mezzo

*Come* utente,

*Voglio* sbloccare uno o più mezzi disponibili,

*Così da* avviare fisicamente la corsa.

### IF-UT.04 – Termina Corsa 

*Come* utente,

*Voglio* terminare la corsa

*Così da* liberare il mezzo.

### IF-UT.05 – Effettua Pagamento

*Come* utente,

*voglio* che il sistema addebiti automaticamente l'importo dovuto sul mio metodo di pagamento predefinito al termine di un'operazione soggetta a pagamento,

*così da* non dover effettuare transazioni manuali ogni volta che utilizzo un servizio a pagamento.

### IF-UT.06 – Salva Metodi Pagamento 

*Come* utente,

*Voglio* salvare uno o più metodi di pagamento,

*Così* *da* ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati.

### IF-UT.07 – Consulta tariffe

*Come* utente,

*Voglio* consultare il tariffario per ciascuna tipologia di mezzo,

*Così da* confrontarne i costi

### IF-UT.08 – Visualizza Riepilogo corsa

*Come* utente,

*Voglio* ricevere il riepilogo corsa,

*Così* da visualizzare le informazioni sulla corsa effettuata

### IF-UT.09 – Sospende Corsa 

*Come* utente,

*Voglio* mettere in pausa la corsa,

*Così da* effettuare soste senza perdere il possesso del mezzo.

### IF-UT.10 – Visualizza Promozioni 

*Come* utente,

*Voglio* accedere alle promozioni attive,

*Così* da ridurre i costi di utilizzo del servizio.

### IF-UT.11 – Visualizza Storico Corsa 

*Come* utente,

*Voglio* visualizzare lo storico delle corse,

*Così* *da* tenere traccia di tutte le corse effettuate.

### IF-UT.12 – Invia Segnalazione 

*Come* utente,

*Voglio* inviare una segnalazione,

*Così* da informare l'operatore affinché possa intervenire.

### IF-UT.13 – Sottoscrive Abbonamento 

*Come* utente,

*Voglio* sottoscrivere un abbonamento,

*Così* *da* usufruire di condizioni tariffarie agevolate.

### IF-UT.14 – Visualizza Suggerimenti Intelligenti

*Come* utente,

*Voglio* visualizzare suggerimenti intelligenti calcolati dal sistema,

*Così da* individuare opportunità di risparmio economico sulla base delle mie abitudini di mobilità.

### IF-UT.15 – Scrive una recensione 

*Come* utente,

*Voglio* lasciare una recensione,

*Così da* aiutare a migliorare il servizio.

###  IF-AP.01 – Accede Report

*Come* amministrazione pubblica,

*Voglio* accedere a report aggregati sull'utilizzo del servizio,

*Così* *da* supportare decisioni strategiche di pianificazione.

### IF-AP.02 – Esporta Report

*Come* amministrazione pubblica,

*Voglio* esportare i report aggregati sull'utilizzo del servizio in Formato Esportabile,

*Così* da utilizzarli in analisi esterne e documentazione ufficiale.

### IF-AP.03 – Visualizza Mappa Amministrazione Pubblica

*Come* amministrazione pubblica,

*Voglio* visualizzare la “Mappa Amministrazione Pubblica”,

*Così* *da* monitorare il servizio sulla città.

### IF-OP.01 – Visualizza Mappa Operatore

*Come* operatore,

*Voglio* visualizzare la “Mappa Operatore”,

*Così* *da* pianificare operazioni di redistribuzione.

### IF-OP.02 – Aggiunge Mezzo

*Come* operatore,

*Voglio* aggiungere un nuovo mezzo alla mappa,

*Così* *da* aumentare il numero di mezzi della flotta.

### IF-OP.03 – Dismette Mezzo

*Come* operatore,

*Voglio* dismettere un mezzo dalla mappa,

*Così* *da* gestire il ciclo di vita della flotta.

### IF-OP.04 – Modifica Stato Mezzo

*Come* operatore,

*Voglio* modificare lo Stato di un mezzo,

*Così* *da* nasconderlo o mostrarlo sulla Mappa Utente.

### IF-OP.05 – Definisce Tariffa

*Come* operatore,

*Voglio* definire la tariffa del servizio,

*Così* *da* permettere la configurazione del modello di costo.

### IF-OP.06 – Definisce Regole Fine Corsa

*Come* Operatore,

*Voglio* definire le regole che si applicano al rilascio dei mezzi a fine corsa,

*Così da* incentivare un comportamento corretto degli utenti e garantire il decoro urbano.

### IF-OP.07 - Definisce Zona

*Come* operatore,

*Voglio* definire i confini di una Zona,

*Così* *da* garantire il rispetto delle normative locali.

### IF-OP.08 – Gestisce Segnalazioni

*Come* operatore,

*Voglio* leggere le segnalazioni inviate dagli utenti,

*Così* *da* pianificare gli interventi di manutenzione.

### IF-OP.09 – Sospende Account Utente

*Come* operatore,

*Voglio* sospendere l'account di un utente,

*Così* *da* tutelare l'integrità del servizio

### IF-OP.10– Definisce Offerte

*Come* operatore,

*Voglio* definire promozioni con condizioni e scadenza configurabili,

*Così* *da* incentivare l'utilizzo del sistema con politiche commerciali flessibili.

### IF-OP.11 – Configura Parametri Numerici di Sistema 

*Come* operatore,

*Voglio* configurare i parametri relativi al sistema,

*Così* da stabilire dei limiti di utilizzo.

### IF-OP.12 – Visualizza Recensioni 

*Come* operatore,

*Voglio* visualizzare le recensioni lasciate dagli utenti,

*così da* avere un riscontro sulle migliorie da apportare al sistema

### IF-OP.13 – Mostra Storico Modifiche

*Come* operatore,

*Voglio* consultare un registro cronologico delle modifiche apportate al sistema,

*Così da* poter ricostruire l'evoluzione delle configurazioni del servizio.

## Item non funzionali

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali.

### Item Informativi

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali di tipo informativo.

#### IIN-1 Prestazioni 

- Il sistema deve aggiornare la posizione dei mezzi sulla Mappa Utente entro 10 secondi

- Il sistema deve completare l'operazione di prenotazione/sblocco di un mezzo entro 15 secondi dalla richiesta dell'utente

#### IIN-2 Sicurezza

- Tutte le comunicazioni tra client e server devono essere cifrate mediante protocolli di sicurezza standard

- Il sistema deve bloccare un account dopo 5 tentativi di autenticazione falliti consecutivi in un tempo configurabile dall’operatore

- I dati personali degli utenti devono essere trattati in conformità al Regolamento UE 2016/679 (GDPR)

- Ciascun ruolo (UT, OP, AP) deve poter accedere esclusivamente alle funzionalità ad esso assegnate

#### IIN-3 Usabilità 

- L'interfaccia deve essere accessibile secondo le linee guida WCAG (es. per utenti con disabilità visive)

- L’interfaccia deve essere facile da usare e comprensibile in meno di 5 minuti

#### IIN-4 Scalabilità 

- L'architettura deve permettere l'aggiunta di nuove tipologie di mezzo senza modifiche strutturali

#### IIN-5 Portabilità 

- Il sistema deve essere accessibile tramite browser web su dispositivi desktop e mobile, senza necessità di installazione

  - L'Utente (UT) accede principalmente da dispositivo mobile (smartphone)

  - L'Operatore (OP) e l'Amministrazione Pubblica (AP) accedono da desktop, data la natura delle operazioni di gestione (mappe, dashboard, report)

#### Conformità

- I report esportabili in CSV/PDF (AP.02) devono rispettare eventuali standard di formato richiesti dalla pubblica amministrazione

### Item di interfaccia

Contiene i requisiti di interfaccia espressi tramite mockup.

#### IUI-1 - Schermata di Login Utente

<img src="media/image1.png" style="width:1.15301in;height:2.05in" alt="Login screen for Smart Mobility app featuring a circular logo with green and blue arrows surrounding a leaf and electric scooter icon. Interface includes username and password fields, login and sign-up buttons, and options to sign in with Google or Apple accounts, with text partially in Italian." />Il mockup illustra l'interfaccia di autenticazione iniziale, caratterizzata da un design *clean* su sfondo bianco. La parte superiore ospita il logo del sistema, sottolineando la vocazione ecosostenibile del brand. Al centro si trova il form di accesso, con campi di input arrotondati per *Username* e *Password*, completato dal link per il recupero credenziali. Le *Call to Action* sono gestite da due grandi pulsanti in verde acqua con ombreggiature ("LOGIN" e "SIGN UP"), seguiti in basso dai collegamenti per il *social login* rapido (Google e Apple).

#### <img src="media/image2.png" style="width:1.18119in;height:2.1in" alt="Map screenshot showing a section of Bari, Italy, with colored markers indicating different transportation options around Politecnico di Bari and Università degli Studi di Bari. Blue markers represent bicycles, green markers indicate scooters, and purple markers show cars, with a red shaded area highlighting Politecnico di Bari and a red location pin marking a specific point nearby." />IUI-2 – Homepage Utente

Questo mockup mostra l'interfaccia cartografica principale dell'app. La top bar offre l'accesso al profilo utente e al menu laterale tramite icona ad hamburger. Al centro, la mappa interattiva geolocalizza in tempo reale la flotta disponibile utilizzando pin codificati per colore e icona (monopattini in verde, bici in blu, auto in magenta). Sulla mappa è visibile un'area evidenziata in rosso (una geo-fence per zone a sosta vietata o velocità limitata) e un marker di posizione. Nella parte inferiore, due pulsanti floating permettono di avviare una "CORSA DI GRUPPO" o lo "SBLOCCA MEZZO". Chiude la schermata una bottom navigation bar per lo spostamento rapido tra le sezioni principali.

#### <img src="media/image3.png" style="width:1.20625in;height:2.14514in" alt="Screenshot of a mobile app menu for a smart mobility service, displaying options in Italian such as Profile, Pricing Plan, Bonuses and Promotions, History, Settings, Wallet, and Guide with corresponding icons. The menu overlays a partial map showing bike icons near Via Giuseppe Re, indicating bike-sharing locations." />IUI-3 – Menu Laterale Utente

Il mockup illustra il *side drawer* (menu laterale a scomparsa) aperto, che scorre da destra sovrapponendosi alla mappa di sfondo, la quale risulta oscurata per mantenere il focus dell'utente. L'intestazione presenta il logotipo del brand affiancato da una chiara icona "X" per la chiusura del pannello. L'architettura dell'elenco voci allinea testo e icone vettoriali (declinate nel verde acqua aziendale) sul lato destro, favorendo una lettura rapida. Le opzioni di navigazione garantiscono l'accesso immediato alle sezioni gestionali e amministrative dell'utente, coprendo l'area personale (*Profilo*, *Impostazioni*, *Guida*) e la sfera economica/operativa (*Piano Tariffario*, *Bonus e Promozioni*, *Cronologia*, *Portafoglio*). Il layout adotta uno spazio bianco generoso per un design pulito e leggibile.

#### IUI-4 – Corsa di Gruppo

<img src="media/image4.png" style="width:1.08819in;height:1.93542in" alt="Screenshot of a mobile app interface for Smart Mobility showing a map with locations of available scooters marked by green and blue icons. The screen displays a group ride initiation status with three out of five scooters unlocked, each listed with unique IDs and battery levels indicated by green and yellow bars." />Il mockup presenta l'interfaccia di gestione per le corse multiple, implementata tramite un pannello a comparsa inferiore (*bottom sheet*) sovrapposto parzialmente alla mappa. L'intestazione, dotata di icona di chiusura rapida, introduce la funzione "Inizia corsa di gruppo" seguita da un contatore dinamico di stato ("Veicoli sbloccati: 3/5"). Il corpo centrale elenca i veicoli già agganciati alla sessione tramite singole *cards* arrotondate; ciascuna scheda fornisce dati in tempo reale mostrando l'icona del mezzo, il codice identificativo alfanumerico e l'indicatore visivo della batteria (con colorazione semantica verde/giallo). Nella parte inferiore è posizionata la *Call to Action* ("SBLOCCA VEICOLO"), un pulsante primario per aggiungere ulteriori mezzi prima dell'avvio definitivo della corsa.

#### <img src="media/image5.png" style="width:1.13403in;height:2.01667in" alt="Screenshot of a scooter rental app interface showing a map with a green location pin indicating scooter availability near Politecnico di Bari. The booking panel displays scooter ID BZ234VF, a full battery icon, and a countdown timer until 16:47 to unlock the scooter, with a green &quot;Prenota&quot; button for reservation." />IUI-5 – Prenotazione Mezzo

Il mockup illustra l'interfaccia per la prenotazione di un singolo veicolo, realizzata tramite un *bottom sheet* che si sovrappone alla mappa. Sulla cartina, il mezzo selezionato è enfatizzato da un *pin* verde ingrandito. Il pannello, intitolato "Prenota mezzo" con relativa icona di chiusura, riepiloga i dati cruciali: tipologia (Monopattino), codice identificativo e stato visivo della batteria. Un testo informativo avvisa chiaramente l'utente del limite temporale esatto entro cui raggiungere e sbloccare il mezzo. Il flusso si conclude con la *Call to Action* "Prenota", un pulsante primario ben delineato che attiva il blocco temporaneo del veicolo, garantendo all'utente un'interazione fluida e priva di ambiguità.

#### <img src="media/image6.png" style="width:1.13403in;height:2.01736in" alt="Screenshot of a tariff pricing chart for different transportation modes, showing costs per kilometer for electric scooter (0.20€/km), bicycle (0.30€/km), and automobile (0.50€/km). The chart uses black icons for each vehicle type alongside green text for labels and prices, with a &quot;SMART MOBILITY&quot; logo below and navigation icons at the bottom." />IUI-6 – Visualizzazione del Piano Tariffario

Questo mockup rappresenta la sezione informativa sui costi del servizio, strutturata con un layout minimale e ampio spazio bianco per massimizzare la leggibilità. L'header presenta il titolo della sezione affiancato da un'icona di chiusura rapida. Al centro, tre *card* dal design a pillola con morbida ombreggiatura illustrano le tariffe chilometriche per ogni categoria di veicolo (Monopattino a 0,20€/km, Bicicletta a 0,30€/km, Automobile a 0,50€/km), accostando icone stilizzate ai relativi costi per un'immediata comprensione visiva. Completa l'interfaccia il logo aziendale centrato nella parte inferiore e la *bottom navigation bar* fissa, che garantisce continuità nell'esplorazione dell'app.

#### <img src="media/image7.png" style="width:1.10139in;height:1.95833in" alt="Screenshot of a digital wallet interface showing a zero balance with payment method options including Google Pay, Apple Pay, PayPal, and credit card addition. The layout features green text and buttons with icons for each payment method and a prominent green button labeled &quot;RICARICA SALDO&quot; for recharging balance." />IUI-7 – Visualizzazione del Saldo e Metodi di Pagamento 

Il mockup illustra l'interfaccia di gestione finanziaria ("Portafoglio"). La gerarchia visiva pone in primo piano una *card* delimitata in verde acqua che evidenzia a grandi caratteri il "Saldo" disponibile. La sezione sottostante dedicata ai "Metodi di Pagamento" è organizzata in un menu a lista provvisto di *chevron* direzionali per suggerire l'interazione. Questo blocco integra opzioni di *digital wallet* (Google Pay, Apple Pay, PayPal) e una voce per l'aggiunta di carte di credito, tutte corredate da loghi o icone di riconoscimento rapido. L'operatività è demandata alla *Call to Action* primaria "RICARICA SALDO", un pulsante *pill-shaped* ad alto contrasto per il *top-up* del conto. Lo stile mantiene il layout pulito dell'applicativo, chiudendosi con la *bottom navigation bar* di sistema.

#### <img src="media/image8.png" style="width:1.31667in;height:2.34236in" alt="Screenshot of a scooter rental app interface displaying trip information. It shows scooter ID BZ234VF, remaining battery level, elapsed time of 46 seconds, and distance traveled of 0.3 kilometers, with buttons to end and pay or pause the ride." />IUI-8 – Schermata Info Corsa

Il mockup illustra il cruscotto di monitoraggio attivo durante il noleggio. L'interfaccia si apre con un'icona circolare in evidenza che identifica la tipologia di veicolo in uso (monopattino). La parte centrale espone la telemetria della sessione in tempo reale tramite un layout tabellare chiaro: riporta l'ID alfanumerico del mezzo, l'indicatore grafico della batteria, il timer del tempo trascorso e i chilometri percorsi. Nella sezione inferiore, sotto il logo aziendale, sono collocate due *Call to Action* operative tramite ampi pulsanti *pill-shaped*. Il sistema offre all'utente il pieno controllo dell'iter di viaggio, consentendo di sospendere temporaneamente la sessione ("PAUSA CORSA") o di concluderla procedendo alla fatturazione ("TERMINA E PAGA").

#### <img src="media/image9.png" style="width:1.38333in;height:2.45903in" alt="Screenshot of a transportation log displaying four entries with icons for electric scooter, bicycle, car, and another electric scooter. Each entry includes ID &quot;BZ345TR,&quot; elapsed time &quot;10:21,&quot; distance traveled &quot;4.98 km,&quot; and date &quot;04/05/2026,&quot; with teal text and icons on a white background." />IUI-9 – Visualizzazione della Cronologia Corse

Il mockup illustra la sezione "Cronologia Corse", progettata per fornire all'utente lo storico dettagliato dei propri noleggi. L'interfaccia adotta un layout a lista lineare, utilizzando divisori orizzontali continui per segmentare visivamente le singole sessioni. Ogni voce (*list item*) espone sulla sinistra un'icona vettoriale identificativa del veicolo (monopattino, bicicletta o automobile), garantendo un riconoscimento visivo immediato. Sulla destra, i dati riepilogativi della corsa sono ordinatamente incolonnati: ID del mezzo, durata ("Tempo trascorso"), distanza ("Km percorsi") e data. Questa architettura dell'informazione modulare e minimalista assicura una facile leggibilità e un'ottima scansionabilità. Chiudono la schermata l'header con comando di chiusura rapida e la *bottom navigation bar* di sistema.

#### IUI-10 – Schermata Login Operatore/Amministrazione Pubblica

Questo mockup illustra l'adattamento landscape (orizzontale) dell'interfaccia di autenticazione, utilizzato da operatore e amministrazione pubblica. Il layout mantiene intatta la coerenza visiva, cromatica e funzionale della controparte mobile, raggruppando gli elementi in un blocco centrale ben allineato. Troviamo in sequenza: il logo, il form di input per Username e Password, i pulsanti primari di LOGIN e SIGN UP, e le opzioni per il social login rapido in basso. L'utilizzo abbondante di spazio bianco (white space) ai lati focalizza l'attenzione dell'utente sull'azione di accesso, garantendo un'esperienza utente pulita e senza distrazioni anche su schermi ampi.<img src="media/image10.png" style="width:2.10347in;height:1.18333in" alt="Login screen screenshot for Smart Mobility app featuring fields for username and password, with buttons for login and sign-up. Includes options to sign in using Google or Apple accounts, and a link for password recovery." />

#### IUI-11 – Dashboard Amministrazione Pubblica

Il mockup illustra la *dashboard* web dedicata all’amministrazione pubblica. Il layout *landscape* è strutturato in due macroaree funzionali: a sinistra, un ampio visualizzatore cartografico interattivo (basato su Google Maps) per il monitoraggio del territorio operativo; a destra, un pannello di controllo lineare che riporta il *branding* aziendale. Le operazioni sono demandate a quattro pulsanti *pill-shaped* ad alto contrasto che consentono la gestione visiva del *geofencing* ("DEFINISCI ZONE VIETATE", "DEFINISCI ZONE LIMITATE", "DEFINISCI ZONE PARCHEGGIO") e l'accesso alle statistiche ("VISUALIZZA REPORT"). L'affiancamento diretto tra la mappa di lavoro e i comandi operativi garantisce all'amministratore un'esperienza utente efficiente e priva di attriti durante il *setup* del servizio cittadino.<img src="media/image11.png" style="width:2.32609in;height:1.30833in" alt="Map combined with user interface buttons showing a section of Bari, Italy, with labeled streets, landmarks, and icons indicating points of interest. Four green buttons on the right side provide options for defining restricted zones, limited zones, parking zones, and viewing reports, suggesting a smart mobility management application." />

#### <img src="media/image12.png" style="width:2.66667in;height:1.4999in" alt="Map showing a restricted zone in Bari outlined by red points, indicating areas where certain vehicles cannot enter. The right panel lists vehicle types with a green checkmark on &quot;Automobile,&quot; highlighting that cars are prohibited from the red zone, while scooters and bicycles are not restricted." />IUI-12 – Definizione Zone Vietate

L'interfaccia illustra il flusso di *geofencing* lato amministratore per la gestione delle aree vietate. Sulla sinistra, la mappa funge da *canvas* interattivo: l'utente posiziona nodi per tracciare un poligono rosso, circoscrivendo visivamente la zona urbana soggetta a restrizione. A destra, un pannello contestuale fornisce istruzioni testuali chiare e coordinate cromaticamente. La parametrizzazione della regola avviene in basso tramite pulsanti *toggle*: l'operatore seleziona a quali veicoli applicare il divieto (es. l'opzione "Automobile" è attiva e confermata da una spunta visibile). Il layout, completato da un'icona di annullamento rapido in alto a destra, sfrutta il paradigma della manipolazione diretta per ottimizzare il *setup* del sistema e ridurre il carico cognitivo.

#### IUI-13 – Definizione Zone Limitate

<img src="media/image13.png" style="width:2.37053in;height:1.33333in" alt="Map showing a restricted zone in Bari outlined by orange points connected with lines, indicating an area where certain vehicles cannot park. A selection panel highlights three vehicle types—scooter, bicycle, and car—with the car option marked as selected, emphasizing vehicle restrictions within the designated zone." />Il mockup mostra la funzionalità amministrativa per la creazione di zone a traffico o velocità limitata. Sfruttando lo stesso paradigma di interazione del tracciamento zone vietate, la mappa permette di disegnare un poligono interattivo tramite nodi. In questo caso, il sistema utilizza semanticamente il colore **arancione** sia per l'area tracciata che per le parole chiave nel testo esplicativo, indicando una restrizione parziale. Il pannello laterale destro consente all'amministratore di selezionare tramite interruttori *toggle* a quale categoria di mezzo applicare la limitazione (nell'esempio, è spuntata "Automobile"). La coerenza visiva e procedurale con le altre schermate di *geofencing* garantisce un'elevata *learnability* del sistema.

#### IUI-14 – Definizione Zone di Parcheggio

<img src="media/image14.png" style="width:2.32609in;height:1.30833in" alt="Map showing parking zone boundaries near Via Celso Ulpiani with green dots marking selected points. Interface includes options to select vehicle types for parking zones, with scooter, bicycle, and car icons, and the car option currently selected." />L'interfaccia illustra la funzione amministrativa dedicata alla mappatura delle aree di sosta. Adottando il medesimo *pattern* d'interazione, la mappa a sinistra consente di tracciare un poligono interattivo, qui declinato semanticamente nel colore **verde** per indicare un'area consentita. A destra, il pannello laterale permette di associare il parcheggio a specifiche categorie di veicoli tramite i consueti controlli *toggle* (nell'esempio, "Automobile").

#### <img src="media/image15.png" style="width:2.475in;height:1.39167in" alt="Bar chart and pie chart displaying weekly and overall distribution of three categories: Monopattini (green), Automobili (pink), and Biciclette (blue). Bar chart shows daily counts with Monopattini highest on Monday and decreasing through the week, while pie chart highlights Monopattini as majority at 55.8%, followed by Biciclette at 31.3%, and Automobili at 11.4%." />IUI-15 – Visualizzazione dei Report

L'interfaccia di reportistica offre all'amministratore una dashboard analitica sull'utilizzo della flotta. La vista si articola in due grafici principali: a sinistra, un istogramma a barre impilate analizza il volume dei noleggi su base settimanale; a destra, un grafico a torta illustra la quota di mercato (in percentuale) per tipologia di mezzo. L'operatività è garantita da due pulsanti in basso che abilitano l'esportazione dei dati in formato CSV e PDF.

#### IUI-16 – Dashboard Operatore

<img src="media/image16.png" style="width:2.51806in;height:1.41597in" />Il mockup illustra la dashboard web dell'operatore con layout split-screen landscape. A sinistra la Mappa Operatore (Google Maps) geolocalizza la flotta tramite pin cromatici per tipologia: monopattini in verde, biciclette in blu, automobili in magenta. In basso sulla mappa due pulsanti floating gestiscono "AGGIUNGI MEZZO" e "DISMETTI MEZZO". Il pannello destro espone sei pulsanti pill-shaped con icone esplicative: "GESTISCI SEGNALAZIONI", "GESTISCI UTENTI", "IMPOSTAZIONI REGOLE", "TARIFFE E PROMOZIONI", "VISUALIZZA REPORT" e "GESTISCI MEZZI". In alto a destra è presente l'icona di accesso al profilo; in basso il logo SMART MOBILITY.

#### IUI-17 – Gestione Segnalazioni

L'interfaccia illustra la schermata dedicata al customer care lato amministratore, strutturata tramite un rigoroso layout tabellare (data grid). Le colonne categorizzano i ticket in entrata esponendo in modo ordinato: identificativo utente, timestamp (data e ora), tipologia di problematica (espressa visivamente tramite icone semantiche per veicoli specifici o alert di sistema) e il dettaglio testuale del disservizio. L'operatività diretta è delegata al pulsante Call to Action "RISPONDI" posto in coda a ciascuna riga, che innesca il flusso di presa in carico del problema.<img src="media/image17.png" style="width:2.5109in;height:1.41228in" alt="Table displaying user reports with columns for user ID, date, time, type, and report details. Entries include a scooter losing power, a car&#39;s right rear light not working, and account issues, with green and white color scheme and response buttons." />

#### <img src="media/image18.png" style="width:2.63542in;height:1.48194in" />IUI-18 – Gestione Tariffe e Promozioni

Il mockup illustra il pannello di configurazione economica del servizio, con layout a due card affiancate e chiusura rapida tramite "X". La card sinistra mostra per ciascuna tipologia di mezzo (Monopattino, Bicicletta, Automobile) un valore numerico editabile e un selettore di unità di misura — evidenziato da un bordo squadrato — che consente all'operatore di scegliere la metrica tariffaria applicata (nell'esempio: €/km). La card destra mostra la promozione attiva tramite un blocco pill-shaped verde acqua e la Call to Action "AGGIUNGI PROMOZIONE".

#### <img src="media/image19.png" style="width:2.65069in;height:1.49097in" alt="Screenshot of a settings panel titled &quot;IMPOSTAZIONI REGOLE&quot; displaying configurable rules for booking and business operations. It includes fields with numerical values for maximum booking duration (30 min), grace period for pause (10 min), maximum concurrent bookings per user (5), tariff percentage during pause (100%), and a dropdown menu with options related to business rules outside parking zones." />IUI-19 – Schermata di Impostazione Regole

Il mockup illustra il pannello amministrativo per la configurazione delle *business rules* di sistema. L'interfaccia adotta una singola e ampia *card* strutturata a lista, dove i parametri operativi sono linearmente modificabili tramite campi di input numerici (es. durata massima della prenotazione, tolleranza della pausa, limiti di prenotazione simultanea per utente e percentuali tariffarie). L'ultima riga mostra un menu a tendina (*dropdown*), qui raffigurato nel suo stato espanso, progettato per selezionare la politica sanzionatoria in caso di sosta fuori zona (penale, divieto o semplice avviso).

### \

Sprint Report N. 3

**Ciclo 4**

**Smart Mobility**

# Sprint Report

## Sprint Backlog

Tabella di riepilogo che indica, per ognuno degli Sprint successivi allo Sprint n.0, la lista degli item del Product Backlog, evidenziando quelli che verranno implementati nell’ambito dello sprint corrente unitamente ad una descrizione esplicativa. Per semplificare l’esposizione e salvaguardare la tracciabilità tra semilavorati si è proceduto alle seguenti assunzioni:

- All’interno di uno Sprint sono implementati un sottoinsieme di item tra quelli specificati nel Product Backlog

- Lo Sprint Backlog relativo allo sprint corrente contiene pertanto l’insieme degli item del Product Backlog in corso di implementazione

- Gli Item funzionali, ovvero le User Stories dovranno essere tracciabili uno a uno, auspicabilmente seppur non necessariamente, con i casi d’uso

- Ad ogni caso d’uso dovrà essere associato uno scenario di base più gli eventuali scenari alternativi. Lo scenario in prima istanza viene redatto a partire dalla specifica della User Story riportata nel Product Backlog

- Ad ogni caso d’uso dovrà essere associato un diagramma di sequenza.

Ogni sprint deve necessariamente produrre in output del codice funzionante. L’unica eccezione è rappresentata dallo Sprint n°0 che deve essere utilizzato per disegnare la macroarchitettura del sistema con le sue componenti e le sue interfacce, e che sarà utilizzata come roadmap per gli sprint successivi andando a chiarire dove si colloca quanto realizzato in ciascuno di essi.

| **Codice Item** | **Numero Sprint** | **Note** |
|----|----|----|
| UT.01 | Sprint 1 | Visualizza Mappa utente |
| UT.02 | Sprint 1 | Prenota mezzo |
| UT.03 | Sprint 1 | Sblocca mezzo |
| UT.04 | Sprint 1 | Termina Corsa |
| UT.05 | Sprint 1 | Effettua Pagamento |
| UT.06 | Sprint 1 | Salva metodo di pagamento |
| AP.01 | Sprint 1 | Accede report |
| OP.01 | Sprint 1 | Visualizza Mappa Operatore |
| OP.02 | Sprint 1 | Aggiunge mezzo |
| OP.03 | Sprint 1 | Dismette mezzo |
| OP.04 | Sprint 1 | Modifica stato mezzo |
| OP.05 | Sprint 1 | Definisce tariffa |
| OP.06 | Sprint 1 | Definisce regole fine corsa |
| OP.07 | Sprint 1 | Definisce Zona |
| UT.07 | Sprint 2 | Consulta Tariffe |
| UT.08 | Sprint 2 | Visualizza Riepilogo Corsa |
| UT.09 | Sprint 2 | Sospende Corsa |
| UT.10 | Sprint 2 | Visualizza Promozioni |
| UT.11 | Sprint 2 | Visualizza Storico Corse |
| UT.12 | Sprint 2 | Invia Segnalazione |
| UT.13 | Sprint 2 | Sottoscrive Abbonamento |
| AP.02 | Sprint 2 | Esporta Report |
| AP.03 | Sprint 2 | Visualizza Mappa Amministrazione Pubblica |
| OP.08 | Sprint 2 | Gestisce Segnalazione |
| OP.09 | Sprint 2 | Sospende Account Utente |
| OP.10 | Sprint 2 | Definisce Offerta |
| OP.11 | Sprint 2 | Configura parametri numerici di sistema |
| UT.14 | Sprint 3 | Visualizza Suggerimenti Intelligenti |
| UT.15 | Sprint 3 | Scrive Recensione |
| OP.12 | Sprint 3 | Visualizza Recensioni |
| OP.13 | Sprint 3 | Mostra storico modifiche |

## Product Requirement Specification 

### Diagramma dei Casi d’uso

<img src="media/image20.png" style="width:4.87531in;height:7.64216in" />

### Specifiche dei Casi d’uso

#### UT – 01 Visualizza Mappa Utente

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Mappa Utente</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema mostra all'Utente autenticato la mappa interattiva con i mezzi disponibili nelle vicinanze, le varie zone, così da poter scegliere un mezzo da prenotare o sbloccare.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L’utente è autenticato alla piattaforma</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'Utente accede alla schermata principale della piattaforma. </p></li>
<li><p>Il sistema rileva la posizione geografica corrente dell'Utente tramite il dispositivo, interrogando ProviderMappa. </p></li>
<li><p>Il sistema recupera i mezzi disponibili e le varie zone (operative, limitate, vietate, parcheggio). </p></li>
<li><p>Il sistema visualizza la mappa con i soli mezzi disponibili per tipologia, le zone, e il marker della posizione corrente.</p></li>
</ol></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La mappa è visualizzata con i dati aggiornati; l'Utente può procedere con la prenotazione o lo sblocco di un mezzo.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>PosizioneNonDisponibile, DatiMappaNonRecuperabili</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza MappaUtente: PosizioneNonDisponibile</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-01.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il dispositivo non supporta la geolocalizzazione o l'Utente nega il permesso; il sistema mostra comunque la mappa centrata su una posizione di default.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>il dispositivo non supporta la geolocalizzazione o l'Utente nega il permesso.</td>
</tr>
<tr>
<td><strong>Post-Condizioni</strong></td>
<td style="text-align: left;">La mappa è visualizzata con i dati aggiornati ma senza il marker di posizione; l'Utente può navigare manualmente la mappa.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. Il sistema rileva che la geolocalizzazione non è disponibile. </p>
<p>2. Il sistema centra la mappa sulla posizione di default. </p>
<p>3. Il sistema prosegue dal passo 3 senza visualizzare il marker della posizione corrente.</p></td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza MappaUtente: DatiMappaNonRecuperabili</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-01.2</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema non riesce a recuperare i dati necessari (mezzi, zone) a causa di un timeout o errore di rete; la mappa non viene visualizzata e l'Utente può riprovare.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Al passo 3: il sistema non riesce a recuperare i dati di mezzi/zone (timeout o errore di rete).</td>
</tr>
<tr>
<td><strong>Post-Condizioni</strong></td>
<td style="text-align: left;">La mappa non viene visualizzata; il caso d'uso termina senza procedere con prenotazione o sblocco.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. Il sistema rileva l'errore nel recupero dei dati. </p>
<p>2. Il sistema mostra un messaggio di errore ("Impossibile caricare i dati della mappa"). </p>
<p>3. Il sistema offre all'Utente la possibilità di riprovare. </p>
<p>4. Se l'Utente riprova, il caso d'uso riparte dal passo 3; altrimenti termina.</p></td>
</tr>
</tbody>
</table>

#### UT – 02 Prenota Mezzo

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Prenota Mezzo</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT - 02</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Utente seleziona uno o più mezzi sulla mappa; per ogni mezzo il sistema mostra le caratteristiche e offre la possibilità di prenotare dei mezzi. Una volta completata la selezione (1 ≤ N ≤ N_max), il sistema avvia la prenotazione di tutti i mezzi scelti.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td><p>1.L'Utente è autenticato</p>
<p>2.Il numero massimo di mezzi prenotabili (N_max ≥ 1) e il raggio di selezione gruppo sono stati configurati dall'Operatore.</p></td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1.Il caso d'uso inizia quando l'Utente vuole prenotare uno o più mezzi sulla mappa.</p>
<p>2.L'Utente seleziona un mezzo disponibile sulla mappa.</p>
<p>3.Il sistema mostra le caratteristiche del mezzo selezionato.</p>
<p>4.Se N &lt; N_max, il sistema offre all'Utente la possibilità di aggiungere altri mezzi nelle vicinanze (entro il raggio configurato dall'Operatore).</p>
<p>5.L'Utente sceglie se aggiungere altri mezzi (torna al passo 2) oppure procedere con la selezione corrente.</p>
<p>6.L'Utente conferma la selezione e avvia la prenotazione.</p>
<p>7.Il sistema verifica che tutti i mezzi selezionati siano ancora disponibili.</p>
<p>8.Per ogni mezzo selezionato, il sistema crea una prenotazione associando il mezzo all'Utente.</p>
<p>9.Per ogni mezzo prenotato, il sistema aggiorna lo stato da "Disponibile" a "Prenotato" e avvia il timer di prenotazione.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Tutti gli N mezzi selezionati risultano nello stato "Prenotato" e associati all'Utente; N timer di prenotazione sono avviati.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>MezzoNonDisponibile</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Prenota Mezzo: MezzoNonDisponibile</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT – 02.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Uno o più dei mezzi selezionati risultano non più disponibili al momento della conferma. Il sistema rimuove dalla selezione solo i mezzi non disponibili e consente all'Utente di sostituirli o di procedere con i restanti.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Almeno un mezzo del gruppo selezionato è passato allo stato "Prenotato" o "In Uso" prima del completamento della richiesta.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>I mezzi ancora disponibili risultano nello stato "Prenotato"; l'Utente non ha prenotazioni attive solo se tutti i mezzi selezionati erano non disponibili.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1.Il caso d’uso inizia dopo il passo 7 della sequenza principale.</p>
<p>2.Il sistema rimuove dalla selezione i mezzi non più disponibili e informa l'Utente.</p>
<p>3.Il sistema mostra la lista aggiornata dei mezzi disponibili nelle vicinanze.</p>
<p>4.L'Utente sceglie se aggiungere un mezzo sostitutivo (torna al passo 2 del flusso principale) oppure procedere con i mezzi rimanenti.</p>
<p>5.Se rimane almeno un mezzo nella selezione, il sistema riprende dal passo 8 del flusso principale.</p>
<p>6.Se la selezione è vuota, il caso d'uso termina senza prenotazioni attive.</p></td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Prenota Mezzo: MezziFuoridalRaggio</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT – 02.2</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Utente tenta di aggiungere un mezzo che si trova oltre il raggio di selezione gruppo configurato dall'Operatore. Il sistema impedisce l'aggiunta e suggerisce mezzi alternativi entro il raggio.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Utente ha già selezionato almeno un mezzo (N ≥ 1) e il raggio di selezione gruppo è stato configurato dall'Operatore.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>La selezione corrente resta invariata; nessun mezzo fuori raggio viene aggiunto.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia dopo il passo 4 della sequenza principale.</p>
<p>2. L'Utente seleziona un mezzo che si trova oltre il raggio di selezione gruppo rispetto al primo mezzo selezionato.</p>
<p>3. Il sistema rileva che la distanza del mezzo supera il raggio configurato e impedisce l'aggiunta alla selezione.</p>
<p>4. Il sistema notifica l'Utente che il mezzo è fuori dal raggio consentito e mostra i mezzi disponibili entro il raggio.</p>
<p>5. L'Utente sceglie se selezionare un mezzo alternativo tra quelli proposti (torna al passo 2 del flusso principale) oppure procedere con la selezione corrente (riprende dal passo 6 del flusso principale).</p></td>
</tr>
</tbody>
</table>

#### UT – 03 Sblocca Mezzo

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th>Nome</th>
<th>Sblocca Mezzo</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT - 03</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Utente avvia la procedura di sblocco fisico di uno o più mezzi; il sistema verifica le condizioni per ciascun mezzo e abilita l'utilizzo di quelli sbloccati con successo.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td><p>1. L'Utente è autenticato;</p>
<p>2.L'Utente si trova in prossimità dei mezzi da sbloccare;</p>
<p>3.Ogni mezzo selezionato è nello stato "Prenotato" dall'Utente corrente oppure nello stato "Disponibile".</p></td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1.Il caso d'uso inizia quando l'Utente vuole sbloccare uno o più mezzi.</p>
<p>2.Il sistema mostra all'Utente i mezzi sbloccabili: quelli con prenotazione attiva a suo nome e quelli disponibili entro un determinato raggio.</p>
<p>3.L'Utente seleziona i mezzi da sbloccare.</p>
<p>4.Per ogni mezzo, il sistema invia il comando di sblocco.</p>
<p>5.Ogni mezzo conferma l'avvenuto sblocco al sistema.</p>
<p>6.Per ogni mezzo sbloccato, il sistema aggiorna lo stato a "In Uso" e registra l'inizio della corsa.</p>
<p>7.Il sistema notifica l'Utente che tutti i mezzi selezionati sono pronti all'uso.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Tutti gli N mezzi selezionati sono fisicamente sbloccati, nello stato "In Uso", con la corsa registrata come avviata.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>SbloccoFallito</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th>Nome</th>
<th>Sblocca Mezzo: SbloccoFallito</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT – 03.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Uno o più mezzi non rispondono al comando di sblocco. Solo i mezzi che non hanno risposto rimangono nel loro stato precedente; gli altri vengono sbloccati regolarmente.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Almeno un mezzo non ha risposto al comando di sblocco entro il timeout.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>I mezzi che hanno risposto sono in stato "In Uso"; i mezzi che non hanno risposto rimangono nel loro stato precedente ("Prenotato" o "Disponibile").</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1.Il caso d’uso inizia dopo il passo 5 della sequenza principale</p>
<p>2.Il sistema rileva il timeout per uno o più mezzi e li rimuove dall'operazione di sblocco.</p>
<p>3.Il sistema notifica l'Utente indicando quali mezzi non è stato possibile sbloccare.</p>
<p>4.L'Utente può riprovare lo sblocco sui mezzi falliti o procedere con quelli già sbloccati.</p></td>
</tr>
</tbody>
</table>

#### UT – 04 Termina corsa

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Termina corsa</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-04</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'utente autenticato di terminare uno o più mezzi della corsa in corso, verificando per ciascun mezzo la posizione e applicando le regole di fine corsa configurate dall'operatore, così da liberare i mezzi e addebitare il costo della sessione.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'utente è autenticato alla piattaforma e ha una o più corse attive.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l'utente seleziona uno o più mezzi della corsa attiva e richiede di terminarli e pagare. </p>
<p>2. Per ciascun mezzo selezionato, il sistema verifica se la sua posizione corrente è all'interno della Zona Operativa. </p>
<p>3. Per ciascun mezzo selezionato, il sistema aggiorna lo stato del mezzo da "In Uso" a "Disponibile" e la corsa a "Terminata". </p>
<p>4. include (EffettuaPagamento) — il pagamento viene elaborato per l'insieme dei mezzi terminati. </p>
<p>5. include (Visualizza Riepilogo Fine Corsa) — il sistema mostra il riepilogo per ciascun mezzo e, se più di uno, il totale complessivo.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Le corse selezionate sono terminate, i mezzi sono liberati e resi disponibili, l'addebito è stato effettuato e il riepilogo è mostrato all'utente.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td style="text-align: left;">MezzoInZonaVietata</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Termina corsa: MezzoInZonaVietata</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-04.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Per uno o più dei mezzi selezionati, il sistema rileva che si trova fuori dalla Zona Operativa (Zona Vietata/Limitata) e applica una penale obbligatoria prima di consentire la fine corsa per quel mezzo.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Almeno uno dei mezzi selezionati si trova fuori dalla Zona Operativa al momento della richiesta di fine corsa.</td>
</tr>
<tr>
<td><strong>Post-Condizioni</strong></td>
<td style="text-align: left;">La corsa relativa al mezzo è terminata con applicazione della penale obbligatoria; il mezzo è liberato e l'addebito con la penale è stato effettuato.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale, per il singolo mezzo interessato. </p>
<p>2. Il sistema rileva che il mezzo si trova fuori dalla Zona Operativa. </p>
<p>3. Il sistema applica la penale obbligatoria al costo della corsa di quel mezzo. </p>
<p>4. Il sistema prosegue dal passo 3 della sequenza principale per quel mezzo.</p></td>
</tr>
</tbody>
</table>

#### UT – 05 Effettua Pagamento

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th>Nome</th>
<th>Effettua Pagamento</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-05</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema addebita un importo definito sul metodo di pagamento predefinito dell'Utente, a seguito di un'operazione che prevede un costo (es. sottoscrizione di abbonamento, termine di una corsa). L'operazione avviene senza richiedere alcuna azione manuale all'utente.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Sistema</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>È stata completata un'operazione soggetta a pagamento</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando il sistema deve procedere all'addebito per un'operazione completata. </p>
<p>2. Il sistema determina l'importo dovuto sulla base delle condizioni economiche applicabili all'operazione (tariffe, piano di abbonamento, eventuale penale, ecc.). </p>
<p>3. Il sistema recupera il metodo di pagamento predefinito dell'Utente. </p>
<p>4. Il sistema trasmette la richiesta di addebito al ProviderPagamenti. </p>
<p>5. Il ProviderPagamenti autorizza e completa la transazione. </p>
<p>6. Il sistema registra il pagamento come completato e restituisce l'esito all'Utente.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'importo è stato addebitato; l'esito del pagamento è mostrato all'Utente.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>PagamentoRifiutato, NessunMetodoPagamento</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th>Nome</th>
<th>EffettuaPagamento: PagamentoRifiutato</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-05.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il ProviderPagamenti rifiuta la transazione.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Sistema</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il ProviderPagamenti ha restituito un esito negativo per la transazione.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>Il pagamento non è andato a buon fine; viene comunque registrato un addebito in sospeso associato all'operazione; l'Utente è notificato del problema e invitato ad aggiornare il metodo di pagamento.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 4 della sequenza principale. </p>
<p>2. Il sistema riceve l'esito negativo dal ProviderPagamenti. </p>
<p>3. Il sistema registra il pagamento come rifiutato. </p>
<p>4. Il sistema notifica l'Utente del fallimento e lo invita ad aggiornare il metodo di pagamento.</p></td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th>Nome</th>
<th>EffettuaPagamento: <strong>NessunMetodoPagamento</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-05.2</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Utente non ha alcun metodo di pagamento salvato (o nessuno impostato come predefinito); l'addebito non può essere tentato.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Sistema</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Utente non ha un metodo di pagamento predefinito disponibile al momento dell'addebito.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>Il pagamento non viene tentato; l'Utente è invitato ad aggiungere un metodo di pagamento.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa sostituisce i passi 3-6 della sequenza principale. </p>
<p>2. Il sistema rileva che l'Utente non ha un metodo di pagamento predefinito. </p>
<p>3. Il sistema notifica l'Utente che deve aggiungere un metodo di pagamento per completare l'operazione.</p></td>
</tr>
</tbody>
</table>

#### UT - 06 Salva Metodo di Pagamento

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>SalvaMetodoDiPagamento</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-06</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'utente autenticato di salvare uno o più metodi di pagamento sul proprio account, così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l'utente accede alla sezione dedicata ai metodi di pagamento dal menu laterale. </p>
<p>2. Il sistema mostra i metodi di pagamento attualmente associati all'account utente e l'opzione per aggiungerne uno nuovo. </p>
<p>3. L'utente seleziona l'opzione per aggiungere un nuovo metodo di pagamento. </p>
<p>4. Il sistema mostra le tipologie di metodo di pagamento disponibili (carta di credito, PayPal, Google Pay, Apple Pay). </p>
<p>5. L'utente seleziona la tipologia desiderata e inserisce i dati richiesti. </p>
<p>6. Il sistema valida i dati inseriti tramite ProviderPagamenti. </p>
<p>7. Il sistema salva il nuovo metodo di pagamento sull'account utente. </p>
<p>8. Se l'utente ha un solo metodo salvato, il sistema lo utilizzerà automaticamente per i futuri addebiti, senza richiedere di impostarlo esplicitamente come predefinito. </p>
<p>9. Se l'utente ha già altri metodi salvati e nessuno è impostato come predefinito, il sistema mostra un avviso nel Portafoglio che invita a impostarne uno come predefinito prima di poter effettuare un pagamento. </p>
<p>10. Il sistema mostra un messaggio di conferma del salvataggio</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il nuovo metodo di pagamento è stato salvato sull'account utente. Se è l'unico metodo presente viene utilizzato automaticamente per gli addebiti; altrimenti l'Utente dovrà impostare esplicitamente un metodo predefinito prima di poter effettuare un pagamento.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td style="text-align: left;">DatiNonValidi, MetodoGiaPresente</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>SalvaMetodoDiPagamento: DatiNonValidi</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-06.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>I dati del metodo di pagamento inseriti dall'Utente non superano la validazione di ProviderPagamenti.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>ProviderPagamenti ha restituito un esito negativo sulla validazione dei dati inseriti.</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il metodo di pagamento non viene salvato; l'Utente può correggere i dati e riprovare.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale. </p>
<p>2. Il sistema rileva l'esito negativo della validazione. </p>
<p>3. Il sistema informa l'Utente che i dati inseriti non sono validi. </p>
<p>4. Il flusso riprende dal passo 5 della sequenza principale.</p></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 28%" />
<col style="width: 71%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>SalvaMetodoDiPagamento: MetodoGiaPresente</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-06.2</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il metodo di pagamento che l'Utente vuole salvare è già associato al proprio account.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il metodo di pagamento validato risulta già presente tra quelli salvati dall'Utente.</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il metodo di pagamento non viene salvato nuovamente; l'Utente è informato della duplicazione.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale. </p>
<p>2. Il sistema rileva che il metodo è già associato all'account.</p>
<p>3. Il sistema informa l'Utente che il metodo è già presente e non procede al salvataggio.</p></td>
</tr>
</tbody>
</table>

#### UT – 07 Consulta Tariffe

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Consulta Tariffe</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-07</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema mostra all'Utente autenticato il tariffario attivo per ciascuna tipologia di mezzo disponibile (Monopattino, Bicicletta, Automobile), indicando il costo al minuto o il costo al chilometro, così da consentirgli di confrontare i costi prima di effettuare una prenotazione.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione "Piano Tariffario" dal menu laterale.</p>
<p>2. Il sistema recupera le tariffe attualmente definite dall'Operatore per ciascuna tipologia di mezzo.</p>
<p>3. Il sistema presenta il tariffario con una card per tipologia di mezzo (Monopattino, Bicicletta, Automobile), indicando per ciascuna il costo al minuto o il costo al chilometro.</p>
<p>4. L'Utente consulta le tariffe visualizzate.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'Utente ha visualizzato il tariffario aggiornato e può procedere con la scelta del mezzo più adatto alle proprie esigenze.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>TariffeNonDefinite</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>ConsultaTariffe: TariffeNonDefinite</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-07.01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Operatore non ha ancora definito le tariffe per una o più tipologie di mezzo.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Non sono presenti tariffe definite dall'Operatore per almeno una tipologia di mezzo.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>Il tariffario non viene mostrato completamente; l'Utente è informato che le tariffe non sono ancora disponibili.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa sostituisce i passi 2 e 3 della sequenza principale.</p>
<p>2. Il sistema verifica che non siano presenti tariffe definite per una o più tipologie di mezzo.</p>
<p>3. Il sistema notifica all'Utente che le tariffe non sono al momento disponibili.</p></td>
</tr>
</tbody>
</table>

#### UT – 08 Visualizza Riepilogo Corsa

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Riepilogo Fine Corsa</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT - 08</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Al termine della procedura di chiusura corsa, il sistema presenta automaticamente all'Utente il riepilogo della sessione appena terminata. In caso di corsa di gruppo, il sistema mostra un riepilogo per ogni mezzo utilizzato e un totale complessivo.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>La procedura Termina Corsa si è conclusa con successo per almeno un mezzo; tutte le corse terminate sono nello stato "Terminata".</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1.Il sistema presenta all'Utente il riepilogo per ogni mezzo.</p>
<p>2.Se la corsa coinvolgeva più di un mezzo:</p>
<p>2.1 il sistema mostra il costo totale complessivo della sessione di gruppo.</p>
<p>3.L'Utente prende visione del riepilogo e lo chiude.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il riepilogo è stato visualizzato; il riepilogo di ogni mezzo è disponibile nello storico corse del profilo.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuna</td>
</tr>
</tbody>
</table>

#### UT – 09 Sospende Corsa

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Sospende corsa</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-09</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'utente autenticato con una corsa attiva di mettere temporaneamente in pausa la corsa, bloccando il mezzo senza terminare la sessione, così da effettuare soste mantenendo il possesso del mezzo. La pausa è gratuita entro il periodo di grazia configurato dall'operatore; al suo termine viene applicata la politica di addebito configurata.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L’utente è autenticato e ha una corsa attiva</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'utente vuole mettere in pausa la corsa in corso.</p>
<p>2. Il sistema invia il comando di blocco temporaneo al mezzo.</p>
<p>3. Il mezzo conferma l'avvenuto blocco al sistema.</p>
<p>4. Il sistema aggiorna lo stato del mezzo da "In Uso" a "In Pausa" e registra l'istante di inizio pausa.</p>
<p>5. Il sistema avvia il conteggio del periodo di grazia configurato dall'operatore.</p>
<p>6. Il sistema notifica all'utente che la corsa è stata sospesa, indicando il tempo di pausa gratuita residuo e l'eventuale politica di addebito successiva.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La corsa non è terminata; il mezzo è bloccato e resta riservato all'utente nello stato "In Pausa"; il sistema mantiene attiva la sessione e traccia la durata della pausa</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Superamento Periodo di Grazia</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>SospendeCorsa: Superamento Periodo di Grazia</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-09.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>La pausa si protrae oltre il periodo di grazia e il sistema applica la politica di addebito per pausa configurata dall'operatore.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>La durata della pausa ha raggiunto il periodo di grazia configurato dall'operatore.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>La corsa resta sospesa con applicazione dell'addebito per pausa secondo la politica configurata; la sessione rimane attiva</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 5 della sequenza principale.</p>
<p>2. Il sistema rileva che la durata della pausa ha raggiunto il periodo di grazia.</p>
<p>3. Il sistema notifica all'utente la fine del periodo di pausa gratuita e l'avvio dell'addebito secondo la politica configurata.</p>
<p>4. Il sistema applica l'addebito per pausa al costo della corsa e prosegue mantenendo il mezzo nello stato "In Pausa".</p></td>
</tr>
</tbody>
</table>

#### UT – 10 Visualizza Promozioni

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Promozioni</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT.10</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema mostra all'Utente autenticato l'elenco delle promozioni attive pubblicate dall'Operatore, con le relative condizioni e vantaggi, così da consentirgli di ridurre i costi di utilizzo del servizio.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione "Bonus e Promozioni" dal menu laterale.</p>
<p>2. Il sistema recupera l'elenco delle promozioni attive pubblicate dall'Operatore.</p>
<p>3. Il sistema presenta l'elenco delle promozioni disponibili, indicando per ciascuna: tipologia, descrizione, condizioni di applicazione e data di scadenza.</p>
<p>4. L'Utente consulta le promozioni disponibili.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'Utente ha visualizzato l'elenco delle promozioni attive e può scegliere di usufruirne nelle corse successive.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>NessunPromozioneAttiva</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>VisualizzaPromozioni: NessunPromozioneAttiva</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-10.01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Non vi sono promozioni attive pubblicate dall'Operatore al momento della richiesta.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Non vi sono promozioni attive pubblicate dall'Operatore.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>L'elenco delle promozioni non viene mostrato; l'Utente è informato dell'assenza di promozioni attive.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa sostituisce i passi 2 e 3 della sequenza principale.</p>
<p>2. Il sistema verifica che non vi siano promozioni attive.</p>
<p>3. Il sistema notifica all'Utente che non sono disponibili promozioni attive al momento.</p></td>
</tr>
</tbody>
</table>

#### UT – 11 Visualizza Storico Corse

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Storico Corse</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT - 11</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'utente consulta l'elenco cronologico delle corse effettuate in passato, con le informazioni di ciascuna.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Utente richiede la visualizzazione dello storico delle corse.</p>
<p>2. Il sistema recupera l'elenco di tutte le corse effettuate dall'Utente.</p>
<p>3. Il sistema presenta l'elenco delle corse effettuate in ordine cronologico.</p>
<p>4. L'Utente consulta le informazioni.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'utente visualizza l'elenco delle corse effettuate con le relative informazioni.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>DatiNonDisponibili</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Storico Corse: DatiNonDisponibili</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT – 11.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema non riesce a recuperare lo storico delle corse a causa di un errore nella disponibilità dei dati.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il sistema non è in grado di accedere ai dati dello storico dell'utente.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>Lo storico non viene mostrato; l'utente è informato del problema temporaneo.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td style="text-align: left;">1.La sequenza alternativa sostituisce i passi 3 e 4 della sequenza principale.<br />
2. Il sistema notifica all'Utente che lo storico delle corse non è al momento disponibile e invita a riprovare.</td>
</tr>
</tbody>
</table>

#### UT – 12 Invia Segnalazione

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Invia segnalazione</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-12</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Utente autenticato di inviare una segnalazione relativa a un mezzo o a una situazione anomala, così da informare l'Operatore affinché possa intervenire tempestivamente.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione dedicata alle segnalazioni.</p>
<p>2. Il sistema mostra il form di segnalazione con i campi richiesti.</p>
<p>3. L'Utente seleziona la tipologia di segnalazione.</p>
<p>4. L'Utente compila i campi richiesti e conferma l'invio.</p>
<p>5. Il sistema registra la segnalazione e la rende visibile all'Operatore.</p>
<p>6. Il sistema notifica l'Utente dell'avvenuto invio della segnalazione.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La segnalazione è registrata nel sistema e resa disponibile all'Operatore per la presa in carico.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuno</td>
</tr>
</tbody>
</table>

#### UT – 13 Sottoscrive Abbonamento

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Sottoscrive Abbonamento</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-13</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Utente autenticato di scegliere e sottoscrivere un piano di abbonamento attivo, così da usufruire di condizioni tariffarie agevolate per un periodo determinato.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td><p>1. L'utente è autenticato alla piattaforma;</p>
<p>2. esistono piani di abbonamento attivi pubblicati dall'operatore</p>
<p>3. l'utente ha un metodo di pagamento valido.</p></td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione dedicata agli abbonamenti.</p>
<p>2. Il sistema recupera e mostra i piani di abbonamento disponibili, con durata, costo e benefici di ciascuno.</p>
<p>3. L'utente seleziona il piano desiderato.</p>
<p>4. Il sistema mostra il riepilogo del piano selezionato e richiede conferma.</p>
<p>5. L'utente conferma la sottoscrizione.</p>
<p>6. Include (EffettuaPagamento)</p>
<p>7. Se il pagamento va a buon fine, il sistema crea e attiva l'abbonamento sull'account dell'utente a partire dalla data corrente. </p>
<p>8. Il sistema notifica l'utente dell'avvenuta attivazione.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'abbonamento è attivo sull'account dell'utente; le condizioni tariffarie agevolate sono applicate a partire dalla data di attivazione. l'addebito del costo del piano è stato effettuato.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>AbbonamentoGiaAttivo</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Sottoscrive Abbonamento: AbbonamentoGiaAttivo</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-13.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Utente tenta di sottoscrivere un nuovo piano mentre ha già un abbonamento attivo; il sistema rifiuta l'operazione.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>l'Utente ha già un abbonamento attivo</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>Nessun nuovo abbonamento viene creato; l'abbonamento corrente resta invariato; l'Utente è informato dell'errore.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa sostituisce i passi 6-8 della sequenza principale. </p>
<p>2. Il sistema rileva che l'Utente ha già un abbonamento attivo. </p>
<p>3. Il sistema rifiuta la richiesta. </p>
<p>4. Il sistema mostra all'Utente il messaggio "Hai già un abbonamento attivo".</p></td>
</tr>
</tbody>
</table>

#### UT – 14 Visualizza Suggerimenti Intelligenti

<table>
<colgroup>
<col style="width: 22%" />
<col style="width: 77%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Suggerimenti Intelligenti</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT – 14</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema raccoglie i dati di utilizzo dell'Utente autenticato e li invia al ServizioAI, che valuta autonomamente se dispone di informazioni sufficienti per produrre suggerimenti personalizzati su prenotazioni, sblocchi, abbonamenti e promozioni. I suggerimenti vengono poi presentati all'Utente così da aiutarlo a ottimizzare l'utilizzo del servizio e individuare opportunità di risparmio economico.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ServizioAI</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>1. L'Utente è autenticato alla piattaforma;</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione "Suggerimenti" della piattaforma.</p>
<p>2. Il sistema raccoglie i dati di utilizzo dell'Utente: storico corse, prenotazioni, orari, zone frequentate, abbonamenti attivi e pagamenti.</p>
<p>3. Il sistema invia i dati aggregati al ServizioAI.</p>
<p>4. Il ServizioAI analizza i dati, valuta autonomamente se sono sufficienti a produrre suggerimenti utili e genera la lista di suggerimenti personalizzati.</p>
<p>5. Il sistema riceve la lista di suggerimenti e la ordina per rilevanza.</p>
<p>6. Il sistema presenta i suggerimenti all'Utente.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>I suggerimenti vengono visualizzati dall'Utente</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>DatiInsufficienti</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Suggerimenti Intelligenti: DatiInsufficienti</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-14.01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il ServizioAI valuta che i dati storici dell'Utente non sono ancora sufficienti per produrre suggerimenti significativi e restituisce una lista vuota con segnale esplicito.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>ServizioAI</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il ServizioAI ha ricevuto i dati dell'Utente e ha determinato autonomamente che non sono sufficienti per generare suggerimenti utili.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>Nessun suggerimento viene mostrato; l'Utente è informato della necessità di continuare a utilizzare il servizio.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa sostituisce i passi 5–6 della sequenza principale.</p>
<p>2. Il ServizioAI restituisce al sistema una lista vuota con un messaggio che indica l’insufficienza dei dati.</p>
<p>3. Il sistema notifica l'Utente che non è ancora possibile generare suggerimenti personalizzati e lo invita a continuare a utilizzare il servizio.</p></td>
</tr>
</tbody>
</table>

#### UT – 15 Scrive Recensione

<table>
<colgroup>
<col style="width: 23%" />
<col style="width: 76%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Scrive Recensione</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT – 15</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Utente accede alla sezione per lasciare recensione dal menu principale e lascia una valutazione (da 1 a 5 stelle) e un commento testuale facoltativo, così da aiutare a migliorare il servizio.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td><p>1. L'Utente è autenticato alla piattaforma;</p>
<p>2. L'Utente ha effettuato e concluso almeno una corsa.</p></td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione per lasciare una recensione dal menu principale.</p>
<p>2. Il sistema mostra il modulo di recensione con campo voto (1–5 stelle) e campo commento testuale facoltativo.</p>
<p>3. L'Utente seleziona un voto da 1 a 5 stelle.</p>
<p>4. L'Utente inserisce facoltativamente un commento testuale.</p>
<p>5. L'Utente conferma l'invio della recensione.</p>
<p>6. Il sistema salva la recensione associandola all'Utente.</p>
<p>7. Il sistema mostra un messaggio di conferma.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La recensione è salvata e associata all'Utente.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><strong>CorsaNonConclusa</strong></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Scrive Recensione: CorsaNonConclusa</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>UT-15.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Utente tenta di inviare una recensione senza aver mai concluso una corsa; il sistema rifiuta l'operazione.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Al passo 6: l'Utente non ha alcuna corsa conclusa.</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La recensione non viene salvata; l'Utente è informato che deve concludere almeno una corsa prima di poter recensire.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia al passo 6 della sequenza principale. </p>
<p>2. Il sistema rileva che l'Utente non ha concluso alcuna corsa. </p>
<p>3. Il sistema rifiuta il salvataggio della recensione. </p>
<p>4. Il sistema mostra all'Utente il messaggio "Devi aver concluso almeno una corsa per lasciare una recensione".</p></td>
</tr>
</tbody>
</table>

#### AP – 01 Accede Report

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Accede Report</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>AP-01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Amministrazione Pubblica autenticata di consultare la dashboard di reportistica aggregata sull'utilizzo del servizio di mobilità condivisa, visualizzando statistiche su corse effettuate, chilometri percorsi e distribuzione per tipologia di mezzo, così da supportare decisioni strategiche di pianificazione urbana.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Amministrazione Pubblica è autenticata alla piattaforma con il ruolo AP.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Amministrazione Pubblica seleziona l'opzione "Visualizza Report" dalla propria dashboard.</p>
<p>2. Il sistema recupera le statistiche aggregate sull'utilizzo del servizio relative all'intervallo temporale configurato.</p>
<p>3. Il sistema presenta la dashboard di reportistica con un istogramma a barre impilate che analizza il volume dei noleggi su base settimanale e un grafico a torta che illustra la quota di mercato per tipologia di mezzo.</p>
<p>4. L'Amministrazione Pubblica consulta i dati visualizzati.</p>
<p>5. Punto di estensione: EsportaReport (si attiva se l'Amministrazione Pubblica seleziona una delle opzioni di esportazione disponibili).</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La dashboard di reportistica è visualizzata con i dati aggregati aggiornati; l'Amministrazione Pubblica ha consultato le statistiche sull'utilizzo del servizio.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>DatiNonDisponibili</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>AccedeReport: DatiNonDisponibili</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>AP-01.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema non riesce a recuperare le statistiche aggregate a causa di un errore nel sistema di elaborazione dati.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il sistema non è in grado di accedere o elaborare i dati aggregati del report.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>La dashboard di reportistica non viene mostrata; l'Amministrazione Pubblica è informata del problema temporaneo.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa sostituisce i passi 2 e 3 della sequenza principale.</p>
<p>2. Il sistema rileva un errore nel recupero dei dati aggregati.</p>
<p>3. Il sistema notifica all'Amministrazione Pubblica che le statistiche non sono al momento disponibili e la invita a riprovare.</p></td>
</tr>
</tbody>
</table>

#### AP - 02 Esporta Report

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Esporta Report</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>AP-02</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Amministrazione Pubblica di esportare il report aggregato correntemente visualizzato in uno dei formati disponibili (CSV o PDF), così da poterlo utilizzare in analisi esterne e documentazione ufficiale. Questo caso d'uso estende AccedeReport.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td><p>L'Amministrazione Pubblica ha acceduto alla dashboard di reportistica.</p>
<p>I dati del report sono disponibili e visualizzati correttamente.</p></td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia dal Punto di estensione EsportaReport di AccedeReport, quando l'Amministrazione</p>
<p>2. Pubblica seleziona una delle opzioni di esportazione disponibili.</p>
<p>3. Il sistema presenta le opzioni di formato disponibili: CSV e PDF.</p>
<p>4. L'Amministrazione Pubblica seleziona il formato desiderato.</p>
<p>5. Il sistema genera il file nel formato selezionato contenente i dati del report aggregato correntemente visualizzato.</p>
<p>6. Il sistema avvia il download del file sul dispositivo dell'Amministrazione Pubblica.</p>
<p>7. Il sistema notifica l'Amministrazione Pubblica del completamento dell'esportazione.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il file del report aggregato è stato generato e scaricato nel formato selezionato; i dati esportati corrispondono alle statistiche visualizzate nella dashboard.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>ErroreGenerazioneFile</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>EsportaReport: ErroreGenerazioneFile</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>AP-02.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema non riesce a generare il file di esportazione nel formato selezionato.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il sistema ha incontrato un errore durante la generazione del file nel formato selezionato.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>Il file non viene generato; l'Amministrazione Pubblica è informata del problema e può ritentare l'operazione.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 4 della sequenza principale.</p>
<p>2. Il sistema rileva un errore nella generazione del file.</p>
<p>3. Il sistema notifica all'Amministrazione Pubblica che l'esportazione non è andata a buon fine.</p>
<p>4. Il sistema invita l'Amministrazione Pubblica a riprovare o a selezionare un formato alternativo.</p></td>
</tr>
</tbody>
</table>

#### AP – 03 Visualizza Mappa Amministrazione Pubblica

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Mappa Amministrazione Pubblica</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>AP-03</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema mostra all'Amministrazione Pubblica autenticata la mappa interattiva dell'area urbana di competenza, arricchita da layer statistici sovrapposti — tra cui la heatmap della distribuzione dei mezzi, l'intensità d'uso per zona e le aree a bassa disponibilità — così da supportare decisioni strategiche di pianificazione e monitoraggio del servizio sul territorio.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Amministrazione Pubblica è autenticata alla piattaforma con il ruolo AP.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Amministrazione Pubblica accede alla schermata principale della propria dashboard. </p>
<p>2. Il sistema recupera i dati geografici di base tramite ProviderMappa e le statistiche aggregate (mezzi, zone, intensità d'uso) relative all'area urbana di competenza. </p>
<p>3. Il sistema carica la mappa interattiva, tramite ProviderMappa, e sovrappone il layer predefinito: la heatmap della distribuzione dei mezzi, che evidenzia con gradiente cromatico le aree ad alta e bassa densità di mezzi disponibili. </p>
<p>4. Il sistema visualizza sulla mappa le zone definite (Operativa, Vietata, Limitata, di Parcheggio) con la rispettiva colorazione semantica. </p>
<p>5. Il sistema mostra nel pannello laterale i layer statistici selezionabili: distribuzione mezzi per tipologia, intensità d'uso per zona e fasce orarie di picco. </p>
<p>6. L'Amministrazione Pubblica seleziona i layer statistici di interesse da visualizzare sulla mappa.</p>
<p>7. Il sistema aggiorna la mappa mostrando i layer selezionati. </p>
<p>8. L'Amministrazione Pubblica consulta i dati territoriali visualizzati.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La mappa è visualizzata con i layer statistici selezionati e aggiornati; l'Amministrazione Pubblica può monitorare la distribuzione dei mezzi sul territorio e procedere con decisioni strategiche di pianificazione urbana.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>DatiNonDisponibili</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>VisualizzaMappaAP: DatiNonDisponibili</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>AP-03.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema non riesce a recuperare i dati geografici (da ProviderMappa) o le statistiche aggregate necessari al caricamento della mappa.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>ProviderMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il ProviderMappa ha restituito un errore o non è raggiungibile al momento della richiesta.</td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>La mappa non viene caricata; l'Amministrazione Pubblica è informata dell'indisponibilità temporanea del servizio cartografico.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale. </p>
<p>2. Il sistema rileva che non è stato possibile recuperare i dati necessari. </p>
<p>3. Il sistema notifica all'Amministrazione Pubblica che la mappa non è al momento disponibile e la invita a riprovare.</p></td>
</tr>
</tbody>
</table>

#### OP – 01 Visualizza Mappa Operatore

<table>
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Visualizza Mappa Operatore</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema mostra all'Operatore autenticato la mappa interattiva con l'intera flotta, incluso lo stato di ciascun mezzo (disponibile, in uso, in manutenzione, ecc.), così da poter pianificare operazioni di redistribuzione o manutenzione.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L’operatore è autenticato alla piattaforma</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'Operatore accede alla schermata principale della piattaforma.</p></li>
<li><p>Il sistema interroga il ProviderMappa per recuperare i dati geografici.</p></li>
<li><p>Il sistema recupera le zone con restrizioni, le zone di parcheggio e lo stato aggiornato di tutti i mezzi della flotta.</p></li>
<li><p>Il sistema visualizza la mappa con tutti i mezzi, lo stato di ciascuno, le aree con restrizioni e il marker della posizione corrente.</p></li>
</ol></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La mappa è visualizzata con i dati aggiornati sull'intera flotta; l'Operatore può procedere con la pianificazione di operazioni di redistribuzione o manutenzione.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuna</td>
</tr>
</tbody>
</table>

#### OP – 02 Aggiunge Mezzo

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Aggiunge Mezzo</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP – 02</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'operatore autenticato di aggiungere un nuovo mezzo alla flotta, specificando tipologia, identificativo, posizione iniziale e stato, così da renderlo disponibile per il noleggio da parte degli utenti.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ProviderMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore è autenticato alla piattaforma e si trova nella Dashboard Operatore.</td>
</tr>
<tr>
<td><strong>Sequenza principale</strong></td>
<td><p>1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata ai mezzi.</p>
<p>2. Il sistema mostra la lista dei mezzi attualmente presenti nella flotta.</p>
<p>3. L'operatore seleziona la funzione che permette di aggiungere un nuovo mezzo.</p>
<p>4. Il sistema permette di inserire i campi: tipologia (monopattino, bicicletta, automobile), identificativo, posizione iniziale e stato iniziale.</p>
<p>5. L'operatore inserisce i dati richiesti e seleziona la posizione iniziale sulla mappa.</p>
<p>6. L'operatore conferma i dati inseriti.</p>
<p>7. Il sistema valida i dati verificando che i campi obbligatori siano compilati e che l'identificativo sia univoco. Se uno o più campi non sono validi, il sistema informa l'operatore specificando i campi non validi e torna al passo 5.</p>
<p>8. Il sistema verifica tramite ProviderMappa che la posizione selezionata ricada all'interno di una zona operativa.</p>
<p>9. Il sistema salva il nuovo mezzo associandolo alla flotta.</p>
<p>10. Il sistema mostra un messaggio di conferma all'operatore.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il nuovo mezzo è stato salvato nel sistema e risulta disponibile sulla Mappa Utente in base allo stato impostato.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>IdentificativoEsistente</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Aggiunge Mezzo: IdentificativoEsistente</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP – 02.01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema rileva che l'identificativo inserito è già associato ad un altro mezzo e segnala l’errore, impedendo il salvataggio.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'identificativo inserito dall'operatore esiste già.</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il nuovo mezzo non viene salvato; l'operatore rimane sulla schermata di inserimento per correggere i dati.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia al passo 7 della sequenza principale.</p>
<p>2. Il sistema verifica l'unicità dell'identificativo.</p>
<p>3. Il sistema rileva che l'identificativo è già presente.</p>
<p>4. Il sistema informa l'operatore dell'errore e torna al passo 5.</p></td>
</tr>
</tbody>
</table>

#### OP – 03 Dismette Mezzo

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Dismette Mezzo</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP – 03</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'operatore autenticato di dismettere un mezzo precedentemente censito, rimuovendone la disponibilità per l'assegnazione a nuove missioni e mantenendone lo storico ai fini di consultazione.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore deve essere autenticato nel sistema e il mezzo da dismettere deve essere già censito e non assegnato ad alcuna missione attiva.</td>
</tr>
<tr>
<td><strong>Sequenza principale</strong></td>
<td><p>1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata ai mezzi.</p>
<p>2. Il sistema mostra la lista dei mezzi presenti nella flotta con il loro stato corrente.</p>
<p>3. L'operatore seleziona il mezzo da dismettere.</p>
<p>4. Il sistema mostra i dettagli del mezzo selezionato e richiede conferma della dismissione.</p>
<p>5. L'operatore conferma la dismissione.</p>
<p>6. Il sistema aggiorna lo stato del mezzo a "Dismesso" e lo rimuove dall'elenco dei mezzi disponibili.</p>
<p>7. Il sistema mantiene lo storico delle informazioni associate al mezzo.</p>
<p>8. Il sistema mostra un messaggio di conferma all'operatore.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il mezzo è registrato come dismesso nel sistema, non risulta più disponibile per l'assegnazione a nuove corse e i dati storici relativi al mezzo rimangono consultabili.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>MezzoInUso</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Dismette Mezzo: MezzoInUso</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-03.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema informa l'operatore che il mezzo selezionato è attualmente impegnato in una missione e non può essere dismesso.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore deve essere autenticato nel sistema e il mezzo selezionato risulta assegnato a una corsa attiva.</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Lo stato del mezzo resta invariato e l'operatore rimane nella sezione di gestione dei mezzi.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. Il sistema, tramite il ProviderMappa, rileva che il mezzo selezionato è impegnato in una corsa.</p>
<p>2. Il sistema notifica all'operatore l'impossibilità di dismettere il mezzo, indicandone la causa.</p>
<p>3. L'operatore prende visione del messaggio e ritorna alla sezione di gestione dei mezzi.</p></td>
</tr>
</tbody>
</table>

#### OP – 04 Modifica stato mezzo

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Modifica Stato Mezzo</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-04</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'operatore autenticato di modificare lo stato di un mezzo della flotta, così da nasconderlo o mostrarlo sulla Mappa Utente e gestire il ciclo operativo del veicolo.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore è autenticato alla piattaforma e il mezzo selezionato esiste nella flotta.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata ai mezzi.</p>
<p>2. Il sistema mostra la Mappa Operatore con la lista dei mezzi della flotta e il loro stato corrente.</p>
<p>3. L'operatore seleziona il mezzo di cui intende modificare lo stato.</p>
<p>4. Il sistema mostra lo stato corrente del mezzo e le opzioni di stato selezionabili tra: Disponibile, In manutenzione, Fuori servizio.</p>
<p>5. L'operatore seleziona il nuovo stato desiderato.</p>
<p>6. Il sistema verifica che la transizione di stato richiesta sia consentita.</p>
<p>7. Il sistema aggiorna lo stato del mezzo.</p>
<p>8. Il sistema mostra un messaggio di conferma all'operatore.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Lo stato del mezzo è stato aggiornato. Se il nuovo stato è "In manutenzione" o "Fuori servizio" il mezzo non è più visibile sulla Mappa Utente; se il nuovo stato è "Disponibile" il mezzo è nuovamente visibile sulla Mappa Utente</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>MezzoImpegnato</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Modifica Stato Mezzo: MezzoImpegnato</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-04.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema informa l'operatore che il mezzo selezionato è attualmente impegnato in una corsa (in uso o in pausa) e non può essere modificato.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Il mezzo selezionato ha stato "In uso" o "In pausa" al momento della richiesta di modifica.</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Nessuna. Lo stato del mezzo non viene modificato.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale. </p>
<p>2. Il sistema rileva che il mezzo è impegnato in una corsa attiva. </p>
<p>3. Il sistema informa l'operatore che non è possibile modificare lo stato del mezzo mentre è impegnato</p></td>
</tr>
</tbody>
</table>

#### OP – 05 Definisce tariffa

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Definisce Tariffa</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-05</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'operatore autenticato di definire una nuova tariffa per una specifica tipologia di mezzo, scegliendo se applicare un costo al minuto oppure un costo al chilometro, così da permettere la configurazione del modello di costo del servizio.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore è autenticato alla piattaforma e non esiste già una tariffa definita per la tipologia di mezzo selezionata.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'operatore accede alla sezione dedicata alle tariffe.</p></li>
<li><p>Il sistema mostra le tariffe attualmente definite per ciascuna tipologia di mezzo disponibile.</p></li>
<li><p>L'operatore seleziona la tipologia di mezzo per cui intende definire una nuova tariffa (monopattino, bicicletta, automobile).</p></li>
<li><p>Il sistema mostra il form di inserimento, chiedendo all'operatore di scegliere il tipo di tariffa: costo al minuto o costo al chilometro.</p></li>
<li><p>L'operatore seleziona il tipo di tariffa e inserisce il valore del costo richiesto.</p></li>
<li><p>Il sistema valida il dato inserito verificando che il valore sia numerico e maggiore di zero.</p></li>
<li><p>Il sistema salva la nuova tariffa, associandola alla tipologia di mezzo selezionata e al tipo di costo scelto.</p></li>
<li><p>Il sistema mostra un messaggio di conferma all'operatore.</p></li>
</ol></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La nuova tariffa è stata salvata nel sistema, con il tipo di costo scelto dall'operatore, e sarà applicata alle corse successive effettuate con la tipologia di mezzo selezionata.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>TariffaGiaEsistente</td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Definisce Tariffa: TariffaGiaEsistente</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-05.1</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'Operatore tenta di definire una tariffa per una tipologia di mezzo che ne ha già una attiva; il sistema rifiuta l'operazione</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Al passo 6 (validazione): esiste già una tariffa definita per la tipologia di mezzo selezionata</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Nessuna nuova tariffa viene salvata; la tariffa esistente resta invariata; l'Operatore è informato dell'errore</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>6a. Il sistema rileva che esiste già una tariffa per la tipologia selezionata.</p>
<p>6b. Il sistema rifiuta la richiesta</p>
<p>6c. Il sistema informa l'Operatore che la tariffa esiste già.</p></td>
</tr>
</tbody>
</table>

#### OP-06 Definisce Regole Fine Corsa

<table>
<colgroup>
<col style="width: 27%" />
<col style="width: 72%" />
</colgroup>
<tbody>
<tr>
<td><strong>Nome</strong></td>
<td><strong>Definisce Regole Fine Corsa</strong></td>
</tr>
<tr>
<td><strong>ID</strong></td>
<td>OP-06</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'operatore definisce le regole sanzionatorie e incentivanti che governano la corretta conclusione di una corsa, specificando la politica sanzionatoria applicata al rilascio del mezzo al di fuori delle zone di parcheggio e un eventuale bonus riconosciuto all'utente al raggiungimento di un numero prestabilito di parcheggi corretti, così da garantire il decoro urbano.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore è autenticato nel sistema ed esiste almeno una zona di parcheggio già definita.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata alle Regole Fine Corsa. </p>
<p>2. Il sistema mostra i parametri configurabili correnti. </p>
<p>3. L'operatore configura le regole: </p>
<p>  3.1 stabilisce la politica sanzionatoria applicata al rilascio del mezzo fuori dalle zone di parcheggio (penale, blocco fine corsa o avviso); </p>
<p> 3.1.2 se la politica prevede una penale, inserisce l'importo da addebitare in aggiunta al costo della corsa; </p>
<p>3.2 se intende attivare un incentivo, configura il bonus indicando il numero di parcheggi corretti necessari e il valore del bonus. </p>
<p>4. L'operatore conferma le regole definite. </p>
<p>5. Se i parametri non rientrano negli intervalli ammessi, il sistema informa l'operatore specificando i campi non validi e torna al passo 3. </p>
<p>6. Il sistema salva la nuova configurazione. </p>
<p>7. Il sistema notifica all'operatore l'avvenuta definizione delle regole.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Le nuove regole di fine corsa sono memorizzate nel sistema e vengono applicate a tutte le corse successive.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuna</td>
</tr>
</tbody>
</table>

#### OP-07 Definisce Zona 

<table style="width:100%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 73%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>DefinisceZona</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP - 07</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'operatore definisce i confini geografici di una Zona caratteristica (Vietata, Limitata, di Parcheggio, Confine Operativo); il sistema memorizza la zona e la applica attivamente.</td>
</tr>
<tr>
<td><strong>Attori primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L’operatore è autenticato con il ruolo OP nel sistema</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'operatore intende definire una zona caratteristica all'interno del sistema.</p></li>
<li><p>Il sistema visualizza la mappa interattiva dell'area di competenza con le zone esistenti</p></li>
<li><p>L'operatore disegna il perimetro della zona sulla mappa definendo i vertici del poligono;</p></li>
<li><p>L'operatore conferma la creazione della zona.</p></li>
<li><p>Fintantoché il perimetro non è valido:</p></li>
</ol>
<p>5.1 Il sistema notifica l'operatore del problema rilevato.</p>
<p>5.2 l'operatore corregge il perimetro (torna al passo 3).</p>
<p>6. Il sistema salva la Zona e la rende attiva.</p>
<p>7. Il sistema aggiorna la mappa visibile agli Utenti evidenziando la nuova zona.</p></td>
</tr>
<tr>
<td><strong>Postcondizioni</strong></td>
<td>La nuova Zona creata è persistita nel sistema con il perimetro definito; il sistema la applica alla flotta.</td>
</tr>
<tr>
<td><strong>Sequenze alternative</strong></td>
<td>Nessuna</td>
</tr>
</tbody>
</table>

#### OP-08 Gestisce Segnalazione

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Gestisce segnalazione</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-08</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Operatore autenticato di consultare le segnalazioni inviate dagli Utenti così da pianificare gli opportuni interventi a fronte delle problematiche riscontrate (relative ai mezzi, alle zone di parcheggio o ad altri aspetti del servizio)</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore è autenticato alla piattaforma.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione dedicata alle segnalazioni</p>
<p>2. Il sistema recupera l'elenco delle segnalazioni inviate dagli Utenti.</p>
<p>3. Il sistema presenta l'elenco delle segnalazioni in ordine cronologico, indicando per ciascuna: tipologia, descrizione e data di invio.</p>
<p>4. L'Operatore consulta le segnalazioni visualizzate.</p>
<p>5. L'Operatore seleziona una segnalazione per visualizzarne il dettaglio.</p>
<p>6. Il sistema mostra il dettaglio completo della segnalazione selezionata.</p>
<p>7. L'Operatore prende in carico la segnalazione.</p>
<p>8. Il sistema aggiorna lo stato della segnalazione a "in carico"; l'Utente, consultando la segnalazione, visualizza lo stato aggiornato.</p>
<p>9. L'Operatore, dopo aver gestito la problematica segnalata, segna la segnalazione come risolta.</p>
<p>10. Il sistema verifica che la segnalazione sia nello stato "in carico" e ne aggiorna lo stato a "risolta".</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La segnalazione è stata presa in carico e successivamente risolta dall'Operatore. L'Utente può consultare lo stato aggiornato ("Risolta") nel proprio storico segnalazioni.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuno</td>
</tr>
</tbody>
</table>

#### OP-09 Sospende Account Utente

<table style="width:99%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 72%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Sospende account utente</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-09</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Operatore autenticato di sospendere l'account di un Utente, così da tutelare l'integrità del servizio in caso di comportamenti scorretti o violazioni delle condizioni d'uso.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td><p>1. L'Operatore è autenticato alla piattaforma.</p>
<p>2. L'account dell'Utente da sospendere è attivo.</p></td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione per la gestione degli utenti.</p>
<p>2. Il sistema presenta l'elenco degli utenti registrati. 3. L'Operatore seleziona l'Utente di cui intende sospendere l'account.</p>
<p>4. Il sistema mostra il dettaglio del profilo dell'Utente selezionato.</p>
<p>5. L'Operatore aggiunge una descrizione sulla motivazione della sospensione dell'account e seleziona la durata della sospensione</p>
<p>6. L'Operatore seleziona l'opzione per sospendere Account.</p>
<p>7. Il sistema richiede conferma dell'operazione.</p>
<p>8. L'Operatore conferma la sospensione.</p>
<p>9. Il sistema sospende l'account dell'Utente per la durata indicata, calcolando la data di fine sospensione, e gli impedisce l'accesso alla piattaforma.</p>
<p>10. Il sistema notifica l'Utente dell'avvenuta sospensione del proprio account.</p>
<p>11. Allo scadere della durata, il sistema riattiva automaticamente l'account e notifica l'Utente della riattivazione.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'account dell'Utente è sospeso fino alla data di fine sospensione; l'Utente non può più accedere alla piattaforma finché la sospensione è attiva; l'Utente è stato notificato dell'avvenuta sospensione. Allo scadere della durata l'account torna automaticamente attivo.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuno</td>
</tr>
</tbody>
</table>

#### OP-10 Definisce Offerta

<table style="width:94%;">
<colgroup>
<col style="width: 26%" />
<col style="width: 68%" />
</colgroup>
<thead>
<tr>
<th><strong>Nome</strong></th>
<th><strong>Definisce Offerta</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>ID</strong></td>
<td>OP-10</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Operatore autenticato di creare e pubblicare offerte commerciali (promozioni e piani di abbonamento) con condizioni e scadenza configurabili, così da incentivare l'utilizzo del servizio con politiche commerciali flessibili.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'operatore è autenticato alla piattaforma.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione delle Offerte.</p>
<p>2. Il sistema mostra le offerte attualmente definite (promozioni e piani di abbonamento) con il rispettivo stato (attiva, scaduta, in bozza).</p>
<p>3. L'Operatore seleziona l'opzione per creare una nuova offerta.</p>
<p>4. Il sistema chiede all'Operatore di scegliere la tipologia di offerta da creare: Promozione o Abbonamento.</p>
<p>5. L'Operatore seleziona la tipologia desiderata.</p>
<p>6. Il sistema mostra il form di configurazione specifico per la tipologia scelta.</p>
<p>7. L'Operatore compila i campi richiesti e conferma.</p>
<p>8. l sistema valida i dati inseriti verificando che i valori siano coerenti e completi (importi numerici e maggiori di zero, date di scadenza nel futuro, nome non duplicato). Se non sono corretti, il sistema invita l’operatore a riprovare e si torna al passo 7.</p>
<p>9. Il sistema salva l'offerta e la pubblica rendendola disponibile agli utenti.</p>
<p>10. Il sistema mostra un messaggio di conferma all'Operatore.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'offerta è salvata nel sistema e resa visibile agli utenti nelle sezioni dedicate</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuno</td>
</tr>
</tbody>
</table>

#### OP-11 Configura parametri numerici di sistema

<table style="width:99%;">
<colgroup>
<col style="width: 28%" />
<col style="width: 70%" />
</colgroup>
<tbody>
<tr>
<td><strong>Nome</strong></td>
<td><strong>Configura Parametri Numerici di Sistema</strong></td>
</tr>
<tr>
<td><strong>ID</strong></td>
<td>OP-11</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>L'operatore configura i parametri numerici operativi del sistema.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L’operatore è autenticato nel sistema</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d’uso inizia quando l’operatore accede alla sezione di configurazione dei parametri di sistema.</p>
<p>2. Il sistema recupera e mostra i valori correnti dei parametri.</p>
<p>3. L’operatore inserisce i nuovi valori dei parametri che intende modificare.</p>
<p>4. L’operatore conferma le modifiche.</p>
<p>5. Se il sistema rileva che uno o più valori non rispettano i vincoli di validazione (non numerici, negativi), viene restituito un errore e il caso d’uso riprende al passo 3</p>
<p>6. Altrimenti Il sistema salva i nuovi parametri.</p>
<p>7. Il sistema mostra un messaggio di conferma all’operatore.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>I nuovi parametri numerici sono salvati nel sistema e applicati a tutte le operazioni successive.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuna</td>
</tr>
</tbody>
</table>

#### OP-12 Visualizza Recensioni

<table style="width:99%;">
<colgroup>
<col style="width: 28%" />
<col style="width: 70%" />
</colgroup>
<tbody>
<tr>
<td><strong>Nome</strong></td>
<td><strong>Visualizza Recensioni</strong></td>
</tr>
<tr>
<td><strong>ID</strong></td>
<td>OP-12</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'Operatore autenticato di consultare l'elenco delle recensioni lasciate dagli utenti (voto da 1 a 5, commento testuale e data di creazione), insieme al voto medio aggregato, così da avere un riscontro sulle migliorie da apportare al servizio.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Operatore è autenticato alla piattaforma con il ruolo OP.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione "Recensioni".</p>
<p>2. Il sistema recupera l'elenco delle recensioni pubblicate dagli utenti e calcola il voto medio aggregato.</p>
<p>3. Il sistema presenta l'elenco delle recensioni, indicando per ciascuna il voto, il commento e la data, insieme al voto medio complessivo.</p>
<p>4. L'Operatore consulta le recensioni visualizzate.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'elenco delle recensioni e il voto medio sono visualizzati; l'Operatore ha consultato i feedback degli utenti.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>NessunaRecensione</td>
</tr>
</tbody>
</table>

<table style="width:99%;">
<colgroup>
<col style="width: 28%" />
<col style="width: 70%" />
</colgroup>
<tbody>
<tr>
<td><strong>Nome</strong></td>
<td><strong>Visualizza Recensioni: NessunaRecensione</strong></td>
</tr>
<tr>
<td><strong>ID</strong></td>
<td>OP-12.01</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Non è presente alcuna recensione pubblicata dagli utenti al momento della richiesta.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>Non sono presenti recensioni nel sistema.</td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>L'elenco delle recensioni non viene mostrato; l'Operatore è informato che non sono ancora presenti recensioni.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td><p>1. La sequenza alternativa sostituisce i passi 2 e 3 della sequenza principale.</p>
<p>2. Il sistema verifica che non sia presente alcuna recensione.</p>
<p>3. Il sistema notifica all'Operatore che non sono ancora disponibili recensioni</p></td>
</tr>
</tbody>
</table>

#### OP-13 Mostra storico modifiche

<table style="width:99%;">
<colgroup>
<col style="width: 28%" />
<col style="width: 70%" />
</colgroup>
<tbody>
<tr>
<td><strong>Nome</strong></td>
<td><strong>Mostra Storico Modifiche</strong></td>
</tr>
<tr>
<td><strong>ID</strong></td>
<td>OP-13</td>
</tr>
<tr>
<td><strong>Breve descrizione</strong></td>
<td>Il sistema consente all'operatore autenticato di consultare un registro cronologico delle modifiche apportate alle configurazioni del servizio (ad esempio parametri numerici di sistema, regole di fine corsa, zone operative), così da poter ricostruire l'evoluzione di tali configurazioni nel tempo.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Operatore</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>Nessuno</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L'Operatore è autenticato alla piattaforma con il ruolo OP e si trova nella DashBoard Operatore.</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'operatore accede alla sezione dedicata allo storico delle modifiche.</p></li>
<li><p>Il sistema recupera l'elenco delle modifiche registrate alle configurazioni del servizio, ordinato dalla più recente alla meno recente.</p></li>
<li><p>Il sistema presenta l'elenco indicando per ciascuna voce: data e ora della modifica, tipo di configurazione interessata, operatore autore e descrizione sintetica del cambiamento (valore precedente e nuovo valore, dove applicabile).</p></li>
<li><p>L'operatore consulta lo storico per ricostruire l'evoluzione delle configurazioni.</p></li>
</ol></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Lo stato del sistema non viene modificato; l'operatore ha consultato il registro cronologico delle modifiche.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>Nessuna</td>
</tr>
</tbody>
</table>

## System Architecture

### Diagramma delle Componenti – Diagramma Generale

<img src="media/image21.png" style="width:6.26806in;height:6.38194in" />

#### Client

<img src="media/image22.png" style="width:6.26806in;height:3.38472in" />

#### Server

<img src="media/image23.png" style="width:6.26806in;height:3.82847in" />

### Specifica delle componenti

Il diagramma delle componenti del sistema SmartMobility rappresenta l'architettura software a un livello di astrazione superiore rispetto al diagramma delle classi. Invece di descrivere singole classi con attributi e metodi, mostra i macro-blocchi funzionali del sistema, le interfacce attraverso cui comunicano e il flusso unidirezionale delle dipendenze. L'architettura segue il pattern Client-Server distribuito a livelli (MVC a tre tier) e si compone di due macro-componenti — Client e Server — più quattro sistemi esterni rappresentati come componenti black-box.

### Specifica delle componenti client

Il Client è la Single Page Application che gira nel browser. Non contiene logica di business: presenta dati e raccoglie azioni dell'utente, delegando tutto al server. È suddiviso in due sotto-componenti.

Il componente **View** (24 classi) raccoglie tutte le schermate dell'applicazione, organizzate per ruolo: viste per l'Utente (homepage con mappa, corsa, storico, pagamenti, abbonamenti, segnalazioni, recensioni, profilo), per l'Operatore (gestione flotta, zone, tariffe, offerte, regole, parametri, segnalazioni, utenti, storico modifiche) e per l'Amministrazione Pubblica (dashboard e report). Ogni Vista delega le operazioni al livello sottostante senza mai comunicare direttamente col server.

Il componente **ApiService** (19 classi) funge da gateway tra le viste e il backend. La classe ApiService agisce come Facade centralizzata: gestisce tutte le chiamate HTTP, il token JWT e gli errori. I 18 Service di dominio (AuthService, CorsaService, MapService, PaymentService, ecc.) traducono le operazioni del proprio ambito in chiamate ad ApiService.

#### Specifica delle componenti server

Il Server ospita la logica di controllo, la logica applicativa, l'accesso ai dati e il modello di dominio. È organizzato in quattro sotto-componenti con una gerarchia rigorosa in cui ogni livello comunica solo con quello adiacente.

Il componente **Controller** (19 classi) è il punto d'ingresso delle richieste HTTP. Il FrontController intercetta ogni richiesta, valida l'autenticazione e la instrada. I 18 controller di dominio si limitano a validare l'input e smistare verso la BLL, senza contenere logica applicativa.

Il componente **BLL(Business Logic Layer)** (16 servizi) è il cuore logico del sistema. Contiene tutta la logica di business, le validazioni di dominio e l'orchestrazione dei flussi. Tra i servizi principali: ServizioMobilita governa il ciclo di vita della mobilità ed è l'unico autorizzato a modificare lo stato di un mezzo; ServizioPricing gestisce il calcolo economico con logica di precedenza abbonamento-promozione-tariffa.

Il componente **DAL (Data Access Layer)** (20 classi) isola la BLL dai dettagli di persistenza. Ogni repository gestisce le operazioni CRUD per una singola entità. È l'unico livello che conosce le entità del Model.

Il componente **Model** (22 classi) definisce le entità del dominio come classi ORM pure. Comprende la gerarchia degli attori (Persona → Utente, Operatore, AmministrazionePubblica), le entità operative (Mezzo, Corsa, Prenotazione, Zona), quelle economiche (Tariffa, Pagamento, Offerta, Promozione, Abbonamento), di configurazione (ParametriSistema, RegolaFineCorsa) e di interazione (Segnalazione, Recensione, Notifica, Suggerimento).

#### Specifica delle componenti Servizi Esterni

Quattro componenti black-box completano l'architettura: **Supabase PostgreSQL** (persistenza relazionale con PostGIS), **Google Maps** (geolocalizzazione e geofencing), **Provider Pagamenti** (autorizzazione transazioni) e **Servizio AI** (generazione suggerimenti personalizzati). L'integrazione avviene tramite il pattern Adapter, che consente la sostituzione di un provider senza impatti sulla BLL.

#### Specifica delle interfacce e del flusso di comunicazione

Ogni componente comunica con gli altri esclusivamente tramite interfacce formali. Le otto interfacce principali sono: ApiToView (ApiService → View), ClientToServer (Controller → ApiService, confine REST/HTTPS), BLLToController (BLL → Controller, realizzazione aggregata di tutte le IServizio\*), Repository (DAL → BLL), DALtoDBMS (DBMS → DAL), e le tre interfacce verso i sistemi esterni (BLLtoGoogleMaps, BLLtoProviderPagamenti, BLLtoServizioAI).

Il flusso delle dipendenze è strettamente unidirezionale: View → ApiService → Controller → BLL → DAL → Model, con diramazioni laterali dalla BLL verso i tre servizi esterni e dal DAL verso il DBMS. Nessun componente risale la catena: questa unidirezionalità è la garanzia architettonica fondamentale di manutenibilità e testabilità del sistema.

## Detailed Product Design

### Diagramma delle Classi – Diagramma Generale

<img src="media/image24.png" style="width:6.26806in;height:5.40417in" />

#### Diagramma delle Classi – Client

<img src="media/image25.png" style="width:6.26806in;height:1.90903in" />

#### Diagramma delle Classi – Server

<img src="media/image26.png" style="width:6.26806in;height:3.50347in" />

#### Diagramma delle Classi – View

<img src="media/image27.png" style="width:6.26806in;height:0.70486in" />

#### Diagramma delle Classi – APIService

<img src="media/image28.png" style="width:6.26806in;height:0.94236in" />

#### Diagramma delle Classi – Controller

<img src="media/image29.png" style="width:6.26806in;height:0.82014in" />

#### Diagramma delle Classi – Business Logic Layer

<img src="media/image30.png" style="width:6.26806in;height:1.24236in" />

#### Diagramma delle Classi – Data Access Layer

<img src="media/image31.png" style="width:6.26806in;height:0.56389in" />

#### Diagramma delle Classi – Model

<img src="media/image32.png" style="width:6.26806in;height:0.85347in" />

#### Diagramma delle Classi – Servizi Esterni

<img src="media/image33.png" style="width:2.80958in;height:8.375in" />

### Specifiche delle Classi

Il diagramma delle classi del sistema SmartMobility modella l'intera architettura software secondo un'organizzazione Client-Server a piu livelli, ispirata al pattern architetturale MVC (Model-View-Controller) e al principio di separazione delle responsabilita. Il sistema comprende complessivamente 144 elementi — tra classi, interfacce e adattatori — collegati da 208 relazioni, in prevalenza dipendenze d'uso.

La struttura si articola in due macro-componenti: la componente **Client**, responsabile della presentazione e dell'interazione con l'utente, e la componente **Server**, che ospita la logica di controllo, la logica applicativa, il modello di dominio e l'accesso ai dati.

Il diagramma include inoltre i sistemi esterni con cui la piattaforma si integra (Google Maps, Provider Pagamenti, Servizio AI), rappresentati tramite il pattern Adapter per garantire disaccoppiamento e sostituibilita. Tre ruoli distinti — Utente (UT), Operatore del Servizio (OP) e Amministrazione Pubblica (AP) — attraversano trasversalmente tutti i layer, e le viste, i controller e i servizi sono organizzati di conseguenza.

#### Specifica delle Classi – Client

La componente Client e suddivisa in due sotto-livelli: il livello **View**, che comprende 24 classi, e il livello **Service (API Service Layer)**, che ne comprende 19.

##### **View — Presentation Layer**

**Viste di Autenticazione e Profilo:**

- **VistaLogin **— Gestisce il form di accesso con email e password, la registrazione di un nuovo account e il recupero delle credenziali. Mostra eventuali messaggi di errore in caso di autenticazione fallita.

- **CallbackOAuth **— Intercetta il ritorno dal provider OAuth (Google) al termine del flusso di autenticazione esterna e ne completa la gestione.

- **PrivacyPolicy **— Presenta all'utente l'informativa sulla privacy del servizio.

- **VistaProfiloUtente** — Consente la visualizzazione e la modifica dei dati personali dell'account (nome, cognome, email), con conferma delle modifiche apportate.

**Viste dell’Utente:**

- **VistaHomePageUtente **— Schermata principale dell'utente. Visualizza la mappa interattiva con i mezzi disponibili e le zone, consente la selezione di un mezzo, permette la consultazione delle tariffe e delle promozioni attive e mostra i suggerimenti personalizzati generati dal sistema.

- **VistaCorsa** — Gestisce l'intero ciclo di vita della corsa dal punto di vista dell'interfaccia: sblocco del mezzo, visualizzazione delle informazioni della corsa in tempo reale, sospensione con indicazione del tempo gratuito residuo e dell'eventuale addebito pausa, terminazione e pagamento, riepilogo finale della sessione, e avviso in caso di ingresso in zona vietata.

- **VistaStoricoCorse** — Mostra l'elenco cronologico delle corse concluse dall'utente, con il totale complessivo speso.

- **VistaPagamenti **— Gestisce il portafoglio digitale: elenca i metodi di pagamento salvati, permette di aggiungerne di nuovi, di impostarne uno come predefinito e di visualizzare il riepilogo di un pagamento.

- **VistaAbbonamenti **— Presenta i piani di abbonamento disponibili, consente di selezionarne uno, ne mostra il riepilogo prima della conferma e visualizza l'eventuale abbonamento attivo.

- **VistaSegnalazioneUtente** — Offre il form per inviare una segnalazione, permettendo di selezionare la tipologia e di inserire una descrizione testuale, con conferma dell'avvenuto invio.

- **VistaRecensione** — Permette all'utente di scrivere una recensione con voto e commento dopo una corsa conclusa, e di consultare lo storico delle proprie recensioni.

**Viste dell’Operatore:**

- **VistaMezziOperatore** — Cruscotto di gestione della flotta. L'operatore può visualizzare l'elenco dei mezzi, selezionarne uno per modificarne lo stato, aggiungere un nuovo mezzo alla flotta o richiederne la dismissione.

- **VistaDashboardOperatore** — Schermata principale dell'operatore. Costituisce il punto di accesso alla mappa operativa con la visualizzazione della flotta dei mezzi gestiti e delle zone operative. Consente all'operatore di selezionare e aprire la mappa operativa, dalla quale può poi navigare verso le altre funzionalità di gestione (mezzi, zone, tariffe, offerte, regole, parametri, segnalazioni, utenti).

- **VistaDefinisciZona** — Presenta l'editor cartografico per disegnare una nuova zona sulla mappa, specificandone nome, tipo (operativa, parcheggio, limitata, vietata), coordinate del perimetro ed eventuale limite di velocità.

- **VistaOfferte** — Gestisce il catalogo delle offerte commerciali: l'operatore può visualizzare la lista, creare una nuova offerta scegliendo tra promozione e abbonamento, modificarne i dati o eliminarla.

- **VistaTariffe** — Permette la consultazione delle tariffe correnti e la definizione di nuove tariffe per tipologia di mezzo, specificando costo al minuto e costo al chilometro.

- **VistaImpostazioniRegole** — Consente la configurazione delle regole di fine corsa, inclusa la politica di vincolo, l'importo della penale e i parametri del bonus per parcheggio corretto.

- **VistaParametriSistema** — Mostra i parametri globali del sistema (durata massima prenotazione, periodo di grazia, numero massimo di mezzi per utente, addebito pausa) e permette all'operatore di modificarli.

- **VistaStoricoModifiche** — Visualizza il log cronologico di tutte le modifiche apportate alle configurazioni di sistema.

- **VistaSegnalazioniOperatore** — Elenca le segnalazioni ricevute dagli utenti, consente di selezionarne una per visualizzarne il dettaglio e di prenderla in carico.

- **VistaGestioneUtentiOperatore** — Mostra l'elenco degli utenti registrati, permette di visualizzare il dettaglio di un account e di avviare la procedura di sospensione con motivazione.

- **VistaRecensioniOperatore** — Presenta le recensioni ricevute dagli utenti con il voto medio complessivo.

**Viste dell’Amministrazione Pubblica:**

- **VistaDashboardAP** — Schermata di governance. Visualizza la dashboard con i report aggregati, consente di selezionare il periodo di riferimento e di esportare i dati in formato CSV o PDF.

- **VistaReportAP** — Mostra i dettagli del report, inclusa la quota dominante tra le tipologie di mezzo e il numero totale di corse nel periodo selezionato.

##### **API Service**

Il livello Service lato client funge da gateway tra le viste e il backend. Ogni classe Service incapsula le chiamate HTTP verso i corrispondenti endpoint del server, gestisce la serializzazione/deserializzazione dei dati e restituisce alle viste oggetti di dominio pronti per la visualizzazione. Tutte le classi di questo livello dipendono da ApiService, il componente centrale che gestisce la comunicazione HTTP.

- **ApiService** è il cuore dell'infrastruttura di comunicazione lato client. Mantiene il baseUrl del backend e il token JWT di autenticazione, espone il metodo generico inviaRichiesta per effettuare chiamate verso qualsiasi endpoint, gestisce le risposte HTTP e gli errori, e si occupa di aggiungere automaticamente gli header di autenticazione a ogni richiesta in uscita.

- **AuthService** gestisce il ciclo di vita dell'autenticazione: login con email e password, logout, registrazione di un nuovo utente, modifica dei dati dell'account e verifica dello stato di autenticazione corrente. Mantiene internamente il token JWT e il riferimento all'utente autenticato.

- **MapService** fornisce i dati cartografici differenziati per ruolo: espone metodi separati per ottenere mezzi e zone nella prospettiva dell'utente, dell'operatore e dell'amministrazione pubblica, ciascuno con il livello di dettaglio e i filtri appropriati al ruolo.

- **CorsaService** gestisce le operazioni relative alla corsa: sblocco di uno o più mezzi, terminazione, sospensione, recupero del riepilogo e dello storico corse, e ottenimento della lista dei mezzi sbloccabili in base alla posizione corrente.

- **PrenotazioneService** incapsula le operazioni di prenotazione: creazione (anche multipla), annullamento e recupero delle prenotazioni attive per un utente.

- **PaymentService** gestisce il portafoglio e i pagamenti: elenca e aggiunge metodi di pagamento, imposta quello predefinito, esegue il pagamento di una corsa, e recupera tariffe e promozioni attive per permettere all'utente di valutare le opzioni prima del pagamento.

- **FlottaService** offre all'operatore le funzionalità di gestione della flotta: elenco dei mezzi, aggiunta di un nuovo mezzo con posizione iniziale, modifica dello stato, dismissione, verifica della disponibilità e recupero delle zone di parcheggio con la configurazione associata.

- **ZonaService** espone le operazioni di creazione ed eliminazione di una zona, specificando nome, tipo, coordinate del perimetro e limite di velocita.

- **AbbonamentoService** gestisce la consultazione dei piani di abbonamento disponibili, la sottoscrizione di un abbonamento e il recupero dell'abbonamento attualmente attivo.

- **OffertaService** permette all'operatore di gestire le offerte commerciali: elenco, creazione, modifica ed eliminazione.

- **TariffaService** consente il recupero delle tariffe correnti e la creazione di una nuova tariffa per tipologia di mezzo.

- **SegnalazioneService** copre entrambi i lati del flusso segnalazioni: l'invio e la consultazione da parte dell'utente, e il recupero, il dettaglio e la presa in carico da parte dell'operatore.

- **RecensioneService** gestisce la scrittura di una recensione, il recupero delle proprie recensioni e la visualizzazione aggregata di tutte le recensioni (per l'operatore).

- **GestioneUtentiService** fornisce all'operatore l'elenco degli utenti, il dettaglio di un singolo account e la funzionalità di sospensione.

- **ReportService** permette all'amministrazione pubblica di recuperare un report aggregato per un dato periodo e di esportarlo in formato CSV.

- **SuggerimentiService** gestisce il recupero dei suggerimenti personalizzati per l'utente e la marcatura come "visto" di un suggerimento già consultato.

- **RegoleFineCorsaService** espone la lettura della configurazione corrente delle regole di fine corsa e il salvataggio di una nuova configurazione.

- **ConfigurazioneService** permette il recupero e l'aggiornamento dei parametri globali del sistema.

- **StoricoModificheService** fornisce l'accesso in lettura al log delle modifiche alle configurazioni di sistema.

#### Specifica delle Classi – Server

La componente Server e organizzata in quattro sotto-livelli che seguono una gerarchia rigorosa: **Controller** (19 classi), **Business Logic Layer** (16 classi), **Data Access Layer** (20 classi) e **Model** (22 classi). Ogni livello comunica esclusivamente con quello immediatamente adiacente, senza salti.

##### **Controller**

Il livello Controller riceve le richieste HTTP dal client, ne valida la struttura e le smista verso il servizio di business logic appropriato. I controller non contengono logica applicativa: il loro unico compito e la validazione dell'input e la formattazione della risposta. Tutti i controller dipendono dal FrontController e accedono alla BLL esclusivamente tramite le interfacce di contratto.

- **FrontController** è il punto d'ingresso unico di tutte le richieste: le intercetta, valida l'autenticazione, le instrada verso il controller specifico e gestisce centralmente gli errori non previsti.

- **AccountController** gestisce gli endpoint di autenticazione: login con credenziali, registrazione, accesso OAuth e recupero del profilo corrente.

- **CorsaController** raggruppa gli endpoint del ciclo di vita della corsa e della prenotazione: creazione prenotazione, sblocco, terminazione, pausa, storico, riepilogo e dettaglio di un singolo mezzo.

- **PagamentoController** espone gli endpoint per la gestione del portafoglio (elenco metodi, creazione, impostazione predefinito, rimozione) e per l'elaborazione del pagamento di una corsa.

- **MezzoOperatoreController** gestisce gli endpoint destinati all'operatore per la gestione della flotta: elenco e mappa dei mezzi, aggiunta, verifica e conferma dismissione, modifica stato, e configurazione delle regole di fine corsa.

- **ZoneController** espone la lista, la creazione e l'eliminazione delle zone operative.

- **TariffaController** gestisce la consultazione, la creazione e l'aggiornamento delle tariffe.

- **AbbonamentoController** espone la lista dei piani disponibili, l'abbonamento corrente dell'utente e la sottoscrizione di un nuovo abbonamento.

- **OffertaController** gestisce il CRUD completo delle offerte commerciali: lista, creazione, modifica ed eliminazione.

- **ConfigurazioneController** espone il recupero e la modifica dei parametri di sistema.

- **RegoleFineCorsaController** gestisce la lettura e la definizione delle regole di fine corsa.

- **SegnalazioneUtenteController** espone gli endpoint lato utente per le segnalazioni: elenco delle proprie segnalazioni e invio di una nuova segnalazione.

- **SegnalazioneOPController** espone gli endpoint lato operatore: lista di tutte le segnalazioni, dettaglio e presa in carico.

- **UtentiOPController** gestisce gli endpoint di gestione utenti da parte dell'operatore: elenco, dettaglio e sospensione.

- **RecensioneController** espone la scrittura di una recensione, il recupero delle proprie e la visualizzazione aggregata.

- **AmministrazionePubblicaController** raccoglie gli endpoint dell'AP: generazione ed esportazione report, mappa mezzi e mappa zone nella prospettiva amministrativa.

- **SuggerimentoController** espone il recupero dei suggerimenti e la marcatura come visto.

- **StoricoModificheController** espone il recupero dello storico delle modifiche.

- **HomePageUtenteController** gestisce gli endpoint della homepage utente per la mappa e i mezzi.

##### **BLL – Business Logic Layer**

Il BLL contiene tutta la logica applicativa del sistema. Ogni servizio riceve le richieste dal controller attraverso la propria interfaccia di contratto, applica le regole di business e delega l'accesso ai dati ai repository del DAL. Nessun servizio accede direttamente al database.

- **ServizioUtenti** gestisce la logica di registrazione, autenticazione (incluso **OAuth**), recupero profilo, esportazione dati, cancellazione account, e le operazioni operative di elenco utenti, dettaglio e sospensione

- **ServizioMobilita** è il servizio più complesso del sistema: governa l'intero ciclo di vita della mobilità. Gestisce lo sblocco di uno o più mezzi (assegnando un gruppoCorsaId condiviso in caso di sblocco multiplo), la terminazione della corsa, la sospensione e la ripresa, il recupero dei mezzi sbloccabili in base alla posizione, la gestione della flotta (elenco, aggiunta, verifica e conferma dismissione, modifica stato), il salvataggio delle regole di fine corsa, il recupero dello storico e il calcolo del riepilogo di sessione.

- **ServizioPrenotazione** gestisce la logica di creazione delle prenotazioni (anche multiple), l'annullamento, il recupero delle prenotazioni attive e le caratteristiche del mezzo prenotato.

- **ServizioPricing** è responsabile del calcolo economico: elabora il pagamento di una corsa applicando la logica di precedenza (abbonamento attivo, poi promozione, poi tariffa piena), calcola l'importo in base a tariffa, durata e distanza, gestisce i metodi di pagamento dell'utente e recupera le promozioni attive.

- **ServizioMappa** gestisce la logica di visualizzazione cartografica: restituisce le zone e i mezzi differenziati per ruolo (utente o operatore), crea ed elimina zone e verifica se una posizione ricade all'interno di una zona operativa.

- **ServizioAbbonamento** gestisce la logica degli abbonamenti: recupero dei piani disponibili, verifica dell'abbonamento attivo e sottoscrizione di un nuovo abbonamento con il vincolo che non possano coesistere due abbonamenti attivi contemporaneamente.

- **ServizioOfferta** governa il ciclo di vita delle offerte commerciali: lista, creazione con validazione dei dati, modifica ed eliminazione.

- **ServizioTariffa** gestisce la logica tariffaria: elenco delle tariffe correnti, creazione di una nuova tariffa e aggiornamento di una esistente per tipologia di mezzo.

- **ServizioSegnalazione** gestisce l'intero ciclo delle segnalazioni: registrazione di una nuova segnalazione da parte dell'utente, elenco delle proprie segnalazioni, elenco completo per l'operatore, dettaglio e presa in carico.

- **ServizioRecensione** gestisce la scrittura di recensioni con validazione del voto e verifica che l'utente abbia almeno una corsa conclusa, il recupero delle proprie recensioni e la visualizzazione aggregata.

- **ServizioReport** è il servizio dedicato all'Amministrazione Pubblica: genera report aggregati su un periodo, ne consente l'esportazione CSV e la consultazione dello storico. Internamente aggrega le statistiche sulle corse e le serializza.

- **ServizioSuggerimenti** genera suggerimenti personalizzati per l'utente sulla base del suo storico di utilizzo. Raccoglie dati da più repository (corse, abbonamenti, pagamenti), li invia al servizio AI tramite l'interfaccia **IServizioAI**, e gestisce la persistenza e la marcatura dei suggerimenti.

- **ServizioRegoleFineCorsa** gestisce la lettura e il salvataggio delle regole di fine corsa (tipo vincolo, penale, bonus parcheggio).

- **ServizioParametri** gestisce la lettura e l'aggiornamento dei parametri globali del sistema.

- **ServizioStoricoModifiche** registra ogni modifica apportata alle configurazioni (tipo, descrizione, valore precedente, valore nuovo, operatore) e ne consente il recupero cronologico.

- **ServizioNotifica** è un servizio trasversale utilizzato da altri servizi della BLL per inviare notifiche agli utenti.

##### **DAL – Data Acces Layer**

Il livello DAL isola completamente la logica applicativa dai dettagli di persistenza. Ogni repository è responsabile delle operazioni CRUD e delle query specifiche per una singola entità del dominio, e comunica direttamente con il DBMS tramite l'ORM SQLAlchemy.

- **IRepository** è l'interfaccia generica che definisce il contratto base per tutti i repository: save, update, delete e findById. Ogni repository concreto può estendere questo contratto con metodi specifici per la propria entità.

- **AttoreRepository** gestisce l'accesso al sottosistema degli attori: ricerca per id o email (restituendo la coppia Persona-ruolo), creazione di un nuovo utente, elenco di tutti gli utenti, ricerca puntuale e sospensione di un account**.**

- **UtenteRepository** espone la ricerca puntuale di un utente per id.

- **OperatoreRepository** gestisce le impostazioni specifiche dell'operatore: recupero e aggiornamento di durata massima prenotazione, periodo di grazia e numero massimo mezzi.

- **MezzoRepository** è uno dei repository più ricchi: offre la ricerca puntuale, il filtraggio per mappa (con opzione solo-disponibili), la ricerca dei mezzi sbloccabili in base alla posizione, il filtraggio da una lista di id, l'elenco completo, la verifica di unicità del codice identificativo, la creazione, l'aggiornamento di stato, il blocco e la verifica di corse attive associate.

- **CorsaRepository** gestisce la persistenza delle corse: creazione con associazione a utente, mezzo, prenotazione e gruppo corsa, aggiornamento stato, ricerca del riepilogo, elenco per utente ordinato per data e filtraggio per periodo temporale.

- **PrenotazioneRepository** gestisce le prenotazioni: creazione con durata, aggiornamento stato, e una serie di ricerche mirate — per utente e mezzo, tutte le attive di un utente, qualsiasi attiva per un mezzo, e per id e utente.

- **PagamentoRepository** gestisce i pagamenti e i metodi di pagamento: ricerca per corsa e per utente, salvataggio, elenco metodi per utente e salvataggio di un nuovo metodo.

- **TariffaRepository** gestisce le tariffe: elenco completo, verifica di esistenza per tipologia, creazione e aggiornamento.

- **ZonaRepository** offre l'elenco delle zone (con filtro attive), la ricerca puntuale, la creazione, l'eliminazione e due verifiche geospaziali: se un punto ricade in una zona operativa e se un'area poligonale e contenuta in una zona operativa esistente.

- **AbbonamentoRepository** gestisce la creazione di una sottoscrizione e il recupero dell'abbonamento attivo per un utente.

- **OffertaRepository** espone la lista, la ricerca puntuale, la verifica di unicità del nome, la creazione, l'aggiornamento e l'eliminazione di offerte.

- **PromozioneRepository** fornisce l'elenco delle promozioni attualmente attive.

- **SegnalazioneRepository** gestisce la creazione, la ricerca per utente e globale, la ricerca puntuale e l'aggiornamento dello stato di una segnalazione.

- **RecensioneRepository** gestisce il salvataggio di una recensione, la ricerca per utente e l'elenco completo.

- **NotificaRepository** gestisce la creazione di una notifica e il recupero delle notifiche per utente.

- **SuggerimentoRepository è** il repository più articolato: ricerca per utente, salvataggio singolo e batch, ricerca dei suggerimenti recenti, aggiornamento dello stato e eliminazione massiva per utente.

- **RegoleFineCorsaRepository** gestisce il recupero della regola corrente, il salvataggio, l'elenco completo, l'eliminazione massiva e la creazione di una regola.

- **ParametriSistemaRepository** espone il recupero e il salvataggio dei parametri globali (durata massima prenotazione, periodo di grazia, numero massimo mezzi, addebito pausa).

- **StoricoModificheRepository** gestisce la creazione di un record di modifica e il recupero dell'elenco completo.

##### **Model**

Il livello Model definisce le entità del dominio come classi ORM pure, prive di logica di business. Le relazioni di ereditarietà e composizione tra le entità riflettono la struttura concettuale del dominio di mobilità condivisa.

- **Gerarchia degli attori. Persona** è la classe base astratta che modella un qualsiasi attore del sistema con id, email, nome e cognome. Da essa derivano tre specializzazioni:

  - **Utente**, che aggiunge lo stato dell'account (attivo, sospeso);

  - **Operatore**, che aggiunge matricola e azienda di appartenenza;

  - **AmministrazionePubblica**, che aggiunge il codice ente.

> Questa gerarchia consente al sistema di gestire in modo uniforme l'identità degli attori, differenziandone il comportamento in base al ruolo.

- **Entità della mobilità.**

  - **Mezzo** rappresenta un veicolo della flotta (bici, auto, monopattino elettrico) con la sua posizione geografica (latitudine e longitudine), la tipologia e lo stato corrente (Disponibile, Prenotato, In uso, In pausa, In manutenzione, Fuori servizio).

  - **Prenotazione** modella la riserva temporanea di un mezzo, con data di creazione, scadenza, stato e un flag che indica se fa parte di un gruppo.

  - **Corsa** rappresenta una sessione di utilizzo di un mezzo: traccia ora di inizio e fine, costo totale, stato, distanza percorsa, eventuale gruppo corsa (per sblocchi multipli) e la durata accumulata di pausa in secondi.

  - **Zona** definisce un'area geografica con nome, perimetro (array di coordinate) e tipo (operativa, parcheggio, limitata, vietata).

- **Entità economiche.**

  - **Tariffa** associa a ogni tipologia di mezzo un costo al minuto o un costo al chilometro, con la data dell'ultimo aggiornamento.

  - **Pagamento** registra una transazione con importo effettivo, importo pieno (prima degli sconti), data, stato e l'eventuale riferimento all'offerta applicata.

  - **MetodoPagamento** rappresenta uno strumento di pagamento salvato dall'utente, con tipo e flag predefinito.

  - **Offerta** è la classe base delle offerte commerciali, con nome, descrizione, tipologia (promozione o abbonamento), stato e date di creazione e scadenza.

    - **Promozione** specializza **Offerta** aggiungendo la percentuale di sconto.

    - **Abbonamento** specializza **Offerta** aggiungendo la tipologia di mezzo coperta, il prezzo e la durata in giorni. **AbbonamentoUtente** rappresenta la sottoscrizione concreta di un utente a un piano, con date di inizio e fine.

- **Entità di configurazione e governance.**

  - **ParametriSistema** contiene i parametri globali del sistema: durata massima della prenotazione, periodo di grazia, numero massimo di mezzi contemporanei per utente e costo dell'addebito in pausa.

  - **RegolaFineCorsa** definisce la politica applicata al termine di una corsa: tipo di vincolo, importo della penale per rilascio fuori zona, numero di parcheggi corretti necessari per il bonus e valore del bonus stesso.

  - **StoricoModifiche** registra ogni modifica a una configurazione con tipo, descrizione, valore precedente, valore nuovo, operatore responsabile e data.

- **Entità di interazione e feedback.**

  - **Segnalazione** registra una segnalazione inviata da un utente con tipologia, descrizione, stato (aperta, in carico, risolta) e data.

  - **Recensione** memorizza il feedback dell'utente con voto numerico, commento testuale e data di creazione.

  - **Notifica** modella un messaggio indirizzato a un utente con testo, flag di lettura e data.

  - **Suggerimento** rappresenta un suggerimento personalizzato generato dal sistema AI, con tipo, testo, dati di contesto, stato (nuovo, visto) e data di creazione.

#### Interfacce e comunicazione tra componenti

La comunicazione tra le componenti del sistema segue un flusso unidirezionale strettamente gerarchico, in cui ogni livello interagisce solo con quello immediatamente adiacente.

##### **Client → Server: API Service → Controller**

Le viste del client delegano ogni operazione ai rispettivi Service del livello **API Service**. Questi Service, a loro volta, comunicano con il server attraverso chiamate **HTTP/REST** gestite centralmente da **ApiService**. Ogni richiesta include automaticamente il token **JWT** di autenticazione. La comunicazione client-server avviene quindi come una catena: la Vista invoca il proprio Service, il Service compone la richiesta HTTP e la invia tramite **ApiService**, il **FrontController** sul server la riceve, ne valida l'autenticazione e la instrada verso il Controller specifico. Le 22 dipendenze tra il livello View e il livello Service, e la singola dipendenza tra Service e Controller, riflettono questa struttura.

##### **Controller → BLL:**

La comunicazione tra il livello Controller e il livello BLL e mediata da 15 interfacce di contratto: **IServizioUtenti, IServizioRecensione, IServizioSegnalazione, IServizioSuggerimenti, IServizioReport, IServizioRegoleFineCorsa, IServizioParametri, IServizioAbbonamento, IServizioStoricoModifiche, IServizioOfferta, IServizioTariffa, IServizioPrenotazione, IServizioMobilita, IServizioPricing e IServizioMappa.** Ogni interfaccia dichiara i metodi che il servizio di business logic deve esporre, senza specificarne l'implementazione. I controller dipendono unicamente da queste interfacce (19 dipendenze) e non conoscono le classi concrete della BLL. Simmetricamente, ogni servizio della BLL implementa la propria interfaccia (14 dipendenze di realizzazione). Questo disaccoppiamento consente di sostituire l'implementazione di un servizio senza modificare alcun controller, e rende il sistema aperto all'estensione ma chiuso alla modifica, nel rispetto del principio Open-Closed.

##### **BLL →DAL:**

I servizi della **BLL** accedono ai dati esclusivamente attraverso i repository del **DAL**. Con 30 dipendenze — il numero più alto dell'intero diagramma — questo e il canale di comunicazione più trafficato del sistema. Servizi complessi come **ServizioMobilita** dipendono da sei repository distinti, mentre servizi più focalizzati come **ServizioParametri** ne utilizzano uno solo. L'interfaccia generica **IRepository** definisce il contratto CRUD base; ogni repository concreto la specializza con query specifiche per la propria entità. I repository dipendono a loro volta dalle entità del Model (17 dipendenze) per costruire e restituire gli oggetti di dominio.

##### **Model:**

Il livello Model presenta 22 relazioni interne — ereditarietà, composizione e associazione — che modellano la struttura del dominio. Le principali sono la gerarchia **Persona → Utente / Operatore / AmministrazionePubblica**, la specializzazione **Offerta → Promozione / Abbonamento**, e le associazioni tra **Corsa, Mezzo, Prenotazione e Pagamento** che rappresentano il nucleo operativo della mobilita condivisa.

##### **Integrazione con i sistemi esterni:**

Il sistema si integra con tre servizi esterni attraverso il pattern **Adapter**, che disaccoppia la logica applicativa dalle API di terze parti.

- **GoogleMapsAdapter** implementa l'interfaccia **GoogleMaps** e traduce le chiamate interne in richieste verso le API di **Google Maps** per la geolocalizzazione e la verifica delle zone.

- **ProviderPagamentiAdapter** implementa l'interfaccia **Pagamenti** e gestisce la comunicazione con il gateway di pagamento esterno per l'autorizzazione delle transazioni e la validazione dei dati di pagamento.

- **ServizioAIAdapter** implementa l'interfaccia **IServizioAI** e si occupa di comunicare con il modello di intelligenza artificiale per la generazione dei suggerimenti personalizzati, includendo la valutazione della sufficienza dei dati prima dell'invocazione.

> Grazie a questo pattern, la sostituzione di un provider esterno (ad esempio il passaggio da Google Maps a un diverso servizio cartografico) richiede la sola modifica dell'Adapter corrispondente, senza impatti sulla **BLL** né sul resto del sistema.

##### **DBMS:**

**DBMS — Supabase PostgreSQL** è il servizio esterno di persistenza che si occupa di memorizzare e restituire tutti i dati del sistema: profili degli attori, mezzi, prenotazioni, corse, pagamenti, zone geografiche, offerte e configurazioni operative. Tutti i repository del **Data Access Layer** comunicano esclusivamente con questo servizio per le operazioni di lettura e scrittura dei dati.

### Diagrammi di Sequenza

#### UT - 01 Visualizza Mappa Utente

<img src="media/image34.png" style="width:6.80481in;height:5.3in" />

#### UT - 02 Prenota Mezzo

<img src="media/image35.png" style="width:6.26806in;height:6.58542in" />

#### UT – 03 Sblocca Mezzo

<img src="media/image36.png" style="width:6.26806in;height:7.3875in" />

#### UT – 04 Termina Corsa

<img src="media/image37.png" style="width:6.26806in;height:6.24167in" />

#### UT – 05 Effettua Pagamento

<img src="media/image38.png" style="width:6.26806in;height:5.97708in" />

#### UT – 06 Salva Metodo di Pagamento

<img src="media/image39.png" style="width:6.26806in;height:9.00694in" />

#### UT – 07 Consulta Tariffe

<img src="media/image40.png" style="width:6.26806in;height:3.80903in" />

#### UT – 08 Visualizza Riepilogo Corsa

<img src="media/image41.png" style="width:6.26806in;height:4.25625in" />

#### UT - 09 Sospende Corsa

<img src="media/image42.png" style="width:6.26806in;height:4.91042in" />

#### UT – 10 Visualizza Promozioni

<img src="media/image43.png" style="width:6.26806in;height:3.74444in" />

#### UT – 11 Visualizza Storico Corse

<img src="media/image44.png" style="width:6.26806in;height:5.34097in" />

#### UT – 12 Invia Segnalazione

<img src="media/image45.png" style="width:6.26806in;height:3.66111in" />

#### UT – 13 Sottoscrive Abbonamento

<img src="media/image46.png" style="width:5.47985in;height:8.67708in" />

#### UT – 14 Visualizza Suggerimenti Intelligenti

<img src="media/image47.png" style="width:6.75317in;height:4.8797in" />

#### UT – 15 Scrive Recensione

<img src="media/image48.png" style="width:6.26806in;height:5.41528in" />

#### AP – 01 Accede Report

<img src="media/image49.png" style="width:6.26806in;height:3.85972in" />

#### AP – 02 Esporta Report

<img src="media/image50.png" style="width:6.26806in;height:4.21181in" />

#### AP – 03 Visualizza Mappa Amministrazione Pubblica

<img src="media/image51.png" style="width:6.26806in;height:3.83472in" />

#### OP-01 Visualizza Mappa Operatore\

<img src="media/image52.png" style="width:6.26806in;height:3.31597in" />

#### OP – 02 Aggiunge Mezzo

<img src="media/image53.png" style="width:6.26806in;height:4.93819in" />

#### OP – 03 Dismette Mezzo

<img src="media/image54.png" style="width:6.26806in;height:5.39306in" />

#### OP – 04 Modifica Stato Mezzo

<img src="media/image55.png" style="width:6.26806in;height:5.03611in" />

#### OP – 05 Definisce Tariffa

<img src="media/image56.png" style="width:6.26806in;height:7.61806in" />

#### OP – 06 Definisce Regole fine corsa

<img src="media/image57.png" style="width:6.26806in;height:5.98472in" />

#### OP – 07 Definisce Zona

<img src="media/image58.png" style="width:6.26806in;height:4.89722in" />

#### OP – 08 Gestisce Segnalazione

<img src="media/image59.png" style="width:4.49862in;height:8.53333in" />

#### OP – 09 Sospende account utente

<img src="media/image60.png" style="width:6.26806in;height:7.57708in" />

#### OP – 10 Definisce Offerta

<img src="media/image61.png" style="width:5.46989in;height:8.80769in" />

#### OP – 11 Configura Parametri Numerici Sistema

<img src="media/image62.png" style="width:6.26806in;height:4.8625in" />

#### OP – 12 Visualizza Recensioni

<img src="media/image63.png" style="width:6.26806in;height:3.51736in" />

#### OP – 13 Mostra Storico Modifiche

<img src="media/image64.png" style="width:6.26806in;height:3.0125in" />

## Data modeling and design

Qui va fornita la specifica di tutti i dati e le informazioni scambiate dal sistema in corso di realizzazione con l’utenza di riferimento e/o gli eventuali altri sistemi con cui esso comunica. Deve essere descritto il modello logico della base di dati e la sua struttura fisica.

### Modello logico del Database

<img src="media/image65.png" style="width:6.26806in;height:3.22847in" />

### Struttura fisica del Database

<img src="media/image66.png" style="width:6.26806in;height:5.49722in" />

# Prompt 

## Qualità dei requisiti

La seguente sezione riporta il prompt utilizzato per la convalidazione della qualità delle user story secondo le 14 caratteristiche di qualità definite nel corso. Le user story corrette a seguito di questa analisi sono riportate nel Product Backlog.

> You are a software engineer, specialized in requirements elicitation. In this phase, you need to read the User Stories. You need to read them carefully, evaluate them following the "Quality Verification Characteristics" that
>
> are listed below.
>
> \### Context
>
> The municipality of Zootropolis wishes to introduce a sustainable transport system that integrates various sharing services (e.g., Bike, Car, E-scooter sharing)
>
> The system must operate in an urban environment involving:
>
> \- Users
>
> \- Operators
>
> \- Public authorities
>
> \## Expected Input Format
>
> The user stories and "Quality Verification Characteristics" are written in Italian.
>
> The user stories that will be sent to you will be in this form:
>
> COME \[ruolo\] VOGLIO \[fare qualcosa\] COSÌ CHE \[possa ottenere valore per il business\]
>
> To add more information, what follows is an example of a user story:
>
> \`COME magazziniere
>
> VOGLIO poter filtrare l'archivio ordini secondo la data di ricezione
>
> COSÌ CHE possa consultare gli ordini evasi\`
>
> \## Quality Verification Characteristics
>
> All of them are reported below:
>
> \### 1. Non Ambiguo
>
> Deve esserci un solo modo di interpretare ogni requisito.
>
> Le ambiguità sono create da:
>
> \*\*Acronimi\*\*: gli acronimi devono essere scritti per intero, con l'acronimo tra parentesi.
>
> Esempio scorretto: "Richiedere al cliente di digitare il PIN."
>
> Esempio corretto: "Richiedere al cliente di digitare il Personal Identification Number (PIN)."
>
> \*\*Cattivo uso dei termini\*\*: termini vaghi lasciano spazio a interpretazioni multiple.
>
> Esempio scorretto: "Il sistema dispensa contanti fino a 500 euro a scelta del cliente." Non è chiaro se la somma e digitata liberamente, scelta tra opzioni, arrotondata o rifiutata se fuori soglia.
>
> Esempio corretto: "Il sistema dispensa una somma a scelta del cliente tra quelle proposte: 100, 150, 200, 250, 300, 400, 500 euro."
>
> \*\*Eccessiva sintesi\*\*: una formulazione troppo breve omette dettagli necessari.
>
> Esempio scorretto: "Il sistema mostra 5 movimenti di Deposito o di Conto Corrente quando il cliente chiede l'estratto conto." Non è chiaro quali 5 movimenti vengano mostrati.
>
> Esempio corretto: "Il cliente richiede l'estratto conto indicando il numero di ultimi movimenti desiderati, fino a un massimo di 20, sul conto di deposito o di conto corrente selezionato. Il sistema mostra 5 movimenti per videata. Se il cliente richiede più di 20 movimenti, il sistema riduce il numero a 20 e avverte il cliente."
>
> \### 2. Provabile o Verificabile: Deve essere possibile costruire casi di test corretti e non corretti rispetto a ogni requisito, per verificare che il sistema elabori correttamente i primi e rigetti i secondi.
>
> Elementi che rendono un requisito non provabile:
>
> \- Aggettivi generici: robusto, sicuro, accurato, effettivo, efficiente, espandibile, flessibile, mantenibile, disponibile, amichevole, adeguato.
>
> \- Avverbi generici: velocemente, tranquillamente, tempestivamente.
>
> \- Parole ed acronimi non specifici: ecc., e/o, TBD.
>
> \- Parole generiche: gestire, manipolare.
>
> \- Espressioni generiche: che sia appropriato, come richiesto, se necessario.
>
> \- Pronomi indefiniti: pochi, molti, tanto, spesso, qualche volta, tutti, qualsiasi, alcune, qualcuno.
>
> \- Voci passive: il soggetto riceve l'azione del verbo invece di compierla.
>
> Esempio scorretto: "Il numero di conto digitato dal cliente sarà controllato per esattezza ed esistenza nella base dati."
>
> Esempio corretto: "Il sistema controlla che il numero di conto digitato sia corretto sintatticamente ed esista nella base di dati."
>
> \### 3. Chiaro: Il requisito deve essere conciso, laconico, semplice e preciso. Non deve contenere verbosità o informazioni non necessarie.
>
> Esempio scorretto: "Qualche volta il cliente potrebbe chiedere l'estratto conto del deposito o del conto corrente intestato a lui; in tal caso deve dichiarare il periodo a cui si deve riferire l'estratto conto richiesto ed è necessario chiedere se vuole la stampa su carta o gli basta vederlo sul video."
>
> Esempio corretto: "Il cliente può chiedere l'estratto conto per il periodo che dichiara. Il sistema riporta l'estratto conto, a scelta del cliente, su carta o su video."
>
> \### 4. Corretto: Se un requisito contiene fatti, questi devono essere veri.
>
> Esempio scorretto: "Il costo dell'operazione sarà di 1 euro."
>
> Questo requisito non è corretto per almeno due motivi: le operazioni eseguibili all'ATM non hanno tutte lo stesso prezzo, e il prezzo dipende dalla politica della banca che gestisce l'ATM e dagli accordi con la banca emittente della carta.
>
> \### 5. Comprensibile: I requisiti devono essere grammaticalmente corretti e scritti in stile consistente. Devono essere usati appositi standard terminologici. La parola "deve" deve essere utilizzata al posto di "volere", "bisogna" o "può".
>
> \### 6. Fattibile: I requisiti devono essere realizzabili entro i vincoli esistenti di tempo, denaro e risorse disponibili.
>
> Esempio scorretto: "Il sistema userà un linguaggio naturale nell'interfaccia così che comprenda i comandi espressi in lingua italiana."
>
> Questo requisito richiede un grande investimento di tempo e risorse, con notevole rischio di non essere realizzato con un adeguato livello di affidabilità.
>
> \### 7. Indipendente e Auto-consistente: Per comprendere un requisito non deve essere necessario conoscere nessun altro requisito.
>
> Esempio scorretto:
>
> \- ReqI: "Il sistema elenca tutti gli importi erogabili per il cliente che ha inserito la carta di credito nell'ATM."
>
> \- ReqD: "Essi sono elencati in ordine crescente."
>
> Il pronome "essi" si riferisce agli importi di ReqI. Se l'ordine dei requisiti nello SRS venisse modificato, ReqD diventerebbe incomprensibile.
>
> \### 8. Atomico: Ogni requisito deve contenere un solo elemento tracciabile. Le espressioni che contengono "e" o "ma" devono essere riviste e suddivise
>
> Esempio scorretto: "Il cliente inserisce il PIN, chiede l'erogazione di una somma e l'estratto conto."
>
> Questo requisito ne contiene tre atomici distinti e deve essere suddiviso di conseguenza.
>
> \### 9. Necessario: Un requisito e inutile se nessuna parte interessata ne ha bisogno, oppure se la sua cancellazione non ha alcuna conseguenza sul sistema finale perché non aggiunge informazioni. I requisiti inutili sono quelli che l'analista inserisce nello SRS ritenendoli desiderati dalle parti interessate, senza che nessuna di esse li abbia esplicitamente richiesti.
>
> Esempi di requisiti potenzialmente non necessari:
>
> \- "Tutti i requisiti specificati nello SRS devono essere testati."
>
> \- "Il sistema stampa il nome della filiale che gestisce l'ATM utilizzato dal cliente."
>
> \### 10. Astratto: I requisiti non devono contenere dettagli circa la loro implementazione, salvo che tale dettaglio costituisca un vincolo esplicitamente dichiarato dall'utente. L'implementazione e di interesse del progettista, non degli utenti del sistema.
>
> Esempio: "Il contenuto informativo sarà memorizzato in forma strutturata."
>
> Questo requisito specifica un dettaglio implementativo e deve essere rivisto salvo che rappresenti un vincolo esplicito.
>
> \### 11. Consistente: Tutti i requisiti devono utilizzare termini uguali per esprimere concetti uguali, e nessun requisito deve essere conflittuale con altri.
>
> I conflitti possono essere:
>
> \*\*Diretti\*\*: in una stessa situazione il comportamento del sistema deve essere diverso.
>
> Esempio:
>
> \- ReqX: "L'ATM accetta tutte le carte di credito e il Bancomat emesso da qualsiasi banca."
>
> \- ReqY: "L'ATM accetta i Bancomat emessi dalle banche convenzionate con la banca gestore."
>
> Per eliminare il conflitto e necessario cancellare uno dei due requisiti.
>
> Esempio di terminologia inconsistente e conflitto sul formato:
>
> \- ReqX: "Le date devono essere visualizzate nella forma mm/dd/yyyy."
>
> \- ReqY: "Le date devono essere visualizzate nella forma gg/mm/aaaa."
>
> Possibile correzione con precisazione del contesto:
>
> \- ReqX: "Le date per gli ATM in U.S. devono essere visualizzate nella forma mm/dd/yyyy."
>
> \- ReqY: "Le date per gli ATM in Italia devono essere visualizzate nella forma gg/mm/aaaa."
>
> In alternativa, generalizzando: "Le date saranno visualizzate nel formato definito dall'utente all'installazione."
>
> \*\*Indiretti\*\*: due requisiti non descrivono la stessa situazione ma non è possibile soddisfarli contemporaneamente.
>
> Esempio:
>
> \- ReqX: "Il sistema deve avere l'interfaccia in linguaggio naturale."
>
> \- ReqY: "Il sistema sarà prodotto in due settimane."
>
> Per eliminare il conflitto e necessario rilassare uno dei due requisiti.
>
> \### 12. Non Ridondante: Ogni requisito deve essere espresso una sola volta e non deve sovrapporsi a un altro.
>
> Esempio:
>
> \- ReqX: "Il sistema mette a disposizione un calendario per aiutare a definire le date di intervallo dell'estratto conto richiesto."
>
> \- ReqY: "Il sistema mette a disposizione un calendario ogni volta che si deve digitare una data."
>
> ReqX e un caso particolare di ReqY e deve essere cancellato.
>
> \### 13. Completo: Un requisito deve essere specificato per tutte le condizioni che possono verificarsi.
>
> Esempio:
>
> \- ReqX: "Il sistema non visualizza la data di prelievo."
>
> \- ReqY: "Il sistema non visualizza l'anagrafica del cliente."
>
> Il numero del conto, che non è né una data né un dato anagrafico, viene visualizzato? Il requisito e incompleto perché non copre tutti i casi possibili.
>
> \### 14. Metriche Derivate
>
> \*\*Manutenibile\*\*: un requisito atomico e non ridondante e più facilmente modificabile.
>
> \*\*Tracciabile\*\*: un requisito atomico dotato di identificatore univoco e tracciabile lungo il ciclo di vita del sistema.
>
> \## Output Format
>
> Each Characteristic must be evaluated on a scale from 0 to 5, and a brief reason pointing out the errors must be specified.
>
> What follows is the output's specific structure. Present all the data in a tabular format; each noun between the rectangular parentheses must be in a separate column. Stick with it and do not perform additional formatting or styling outside of what is being specified below:
>
> \- \[Characteristic Name\], \[score\], \[reason\]
>
> At the end, add a mean score, which is the mean of all the scores.

## 

| Name | Score | Reason |
|:---|:---|:---|
| Non Ambiguo | 3 | Termini vaghi non specificati: "suggerimenti intelligenti" (IF-UT.14), "Formato Esportabile" (IF-AP.02), "parametri relativi al sistema" e "limiti di utilizzo" (IF-OP.11). Lo "Stato" del mezzo (IF-OP.04) non enumera gli stati possibili. |
| Provabile o Verificabile | 3 | Obiettivi non testabili: "garantire il decoro urbano" (IF-OP.06), "rispetto delle normative locali" (IF-OP.07), "tutelare l'integrità del servizio" (IF-OP.09). I "suggerimenti intelligenti" (IF-UT.14) non hanno criteri di accettazione verificabili. |
| Chiaro | 4 | Formulazioni in generale concise. |
| Corretto | 5 | Non si rilevano fatti errati o affermazioni false all'interno delle storie. |
| Comprensibile | 5 | Stile consistente e formato user story (COME/VOGLIO/COSÌ) conforme allo standard prescritto. |
| Fattibile | 4 | Requisiti realizzabili entro vincoli ragionevoli. I "suggerimenti intelligenti" (IF-UT.14) richiedono maggiore sforzo implementativo ma restano fattibili. |
| Indipendente e Auto-consistente | 4 | La maggior parte delle storie è autonoma; alcune richiamano concetti condivisi (Mappa, Stato, Zone) ma restano comprensibili singolarmente. |
| Atomico | 4 | Alcune non atomiche: IF-OP.04 "nasconderlo o mostrarlo" (due azioni distinte), IF-OP.10 "condizioni e scadenza configurabili" (uso di "e"). |
| Necessario | 5 | Ogni storia è riconducibile a un attore e a un valore di business specifico; nessun requisito superfluo. |
| Astratto | 4 | Nessun dettaglio implementativo significativo. "Formato Esportabile" resta a livello astratto senza vincolare la tecnologia. |
| Consistente | 5 | Termini uguali per concetti uguali; nessun conflitto diretto o indiretto tra le storie. |
| Non Ridondante | 5 | Ogni requisito è espresso una sola volta; le tre mappe sono viste distinte per attori diversi, non duplicazioni. |
| Completo | 4 | Copertura funzionale ampia degli scenari principali per tutti gli attori. Resta assente la gestione di registrazione/autenticazione utente, requisito centrale. |
| Metriche Derivate | 5 | Tracciabilità garantita da identificatori univoci (IF-xx.yy) e buona manutenibilità grazie all'atomicità prevalente. |

MEAN SCORE: 4,29

## Diagrammi UML

La seguente sezione riporta i prompt utilizzati per I vari diagrammi UML:

### Diagramma delle componenti

> **Ruolo:** Sei un Senior Software Engineer, Architetto del Software e UI/UX Designer per diagrammi tecnici.
>
> **Obiettivo:** Analizzare, validare la correttezza e ottimizzare la resa grafica di un diagramma delle componenti UML preesistente per il sistema "SMART MOBILITY", trasformandolo in un diagramma professionale, ordinato e visivamente impeccabile in formato .drawio.

**Input che ti fornirò a breve:**

- Il diagramma delle componenti attuale (in formato XML .drawio).

- Documento PDF con le linee guida teoriche, pratiche e gli standard grafici aziendali.

**Istruzioni Passo-Passo:**

- **Step 1: Analisi di Correttezza e Coerenza semantica.** Come prima cosa, analizza il diagramma delle componenti fornito e verifica che il mapping dei componenti, le interfacce fornite ("lollipop") e richieste ("socket") e le dipendenze siano tecnicamente corretti e completi. Se noti errori architetturali o discrepanze gravi, fermati immediatamente e segnalameli prima di procedere.

- **Step 2: Ottimizzazione del Layout e Restyling Grafico.** Se l'architettura è corretta, riorganizza il layout visivo del diagramma. Applica i principi di un design pulito e professionale: allinea geometricamente i blocchi, distribuisci equamente gli spazi, evita l'incrocio caotico delle linee di collegamento, usa una palette di colori coerente (sobria e professionale) e uniforma la dimensione dei font e degli stereotipi.

- **Step 3: Generazione Output.** Genera il codice XML (o formato testo strutturato) ottimizzato, pronto per essere incollato o importare direttamente in .drawio.

> **Requisiti Grafici e UML:** Il risultato finale deve essere "bello, pulito e ordinato", seguendo pedissequamente queste regole:

- Allineamento millimetrico dei componenti (griglia pulita).

- Interfacce "lollipop" e "socket" collegate in modo chiaro, senza sovrapposizioni di testo o linee spezzate in modo bizzarro.

- Gerarchia visiva chiara che rifletta l'architettura a layer (es. Presentazione in alto, Logica al centro, Dati in basso).

- Uso di colori di riempimento tenui e codificati per distinguere i vari layer o macro-aree del sistema.

### Diagramma delle classi

> **Ruolo:** Sei un Senior Software Engineer.
>
> **Obiettivo:** Analizzare, validare la correttezza concettuale e ottimizzare la resa grafica del diagramma delle classi preesistente per il sistema "SMART MOBILITY" (docs/Diagrammi/Diagramma Classi.drawio), trasformandolo in un diagramma professionale, ordinato e visivamente impeccabile in formato .drawio.
>
> **Input che ti fornirò a breve:**

- Il diagramma delle classi attuale (in formato XML .drawio).

- Product Backlog, casi d'uso e glossario di dominio, come riferimento per i nomi e le responsabilità delle classi.

> **Istruzioni Passo-Passo:**

- **Step 1: Analisi di Correttezza e Coerenza semantica.** Verifica che le classi, gli attributi, i metodi, le relazioni (associazione, aggregazione, composizione, generalizzazione/ereditarietà, dipendenza) e le molteplicità siano tecnicamente corretti e completi. In particolare:

  - I nomi delle classi devono corrispondere esattamente al glossario di dominio (Corsa, Mezzo, Prenotazione, Zona con sottotipi ZonaOperativa/ZonaParcheggio/ZonaLimitata/ZonaVietata, Segnalazione, Flotta, Tariffa, Promozione, Abbonamento, Bonus) — non Ride, Booking, Vehicle, ecc.

  - Verifica che ogni relazione abbia un senso architetturale reale (es. niente associazioni bidirezionali ridondanti, niente ereditarietà usata al posto di composizione).

  - Verifica la coerenza tra le classi del diagramma e gli ID del Product Backlog (IF-UT.xx, IF-OP.xx, IF-AP.xx) citati in Sprintn3.md § 1.4 — segnala eventuali ID errati, mancanti o riusati in modo inconsistente.

  - Se noti errori architetturali, ridondanze o discrepanze gravi (classi mancanti, relazioni sbagliate, molteplicità incoerenti), **fermati immediatamente e segnalameli prima di procedere** con il restyling.

- **Step 2: Ottimizzazione del Layout e Restyling Grafico.** Se l'architettura è corretta (o dopo aver risolto le discrepanze segnalate), riorganizza il layout visivo del diagramma:

  - Allinea geometricamente le classi su una griglia pulita, raggruppando per macro-area di dominio (es. Utenti/Attori, Mobilità/Mezzi, Prenotazioni/Corse, Pagamenti/Tariffe/Promozioni/Abbonamenti, Zone, Segnalazioni).

  - Evita incroci caotici delle linee di relazione; preferisci percorsi ortogonali puliti.

  - Uniforma stile e posizione delle molteplicità, dei nomi dei ruoli e degli stereotipi.

  - Usa una palette di colori coerente e sobria per distinguere le macro-aree, mantenendo leggibilità di font e icone.

- **Step 3: Generazione Output.** Genera il codice XML ottimizzato, pronto per essere importato direttamente in .drawio.

> **Requisiti Grafici e UML:**

- Allineamento millimetrico delle classi (griglia pulita).

- Relazioni (associazione/aggregazione/composizione/generalizzazione) chiare, senza sovrapposizioni di testo o linee spezzate in modo bizzarro.

- Gerarchia visiva chiara che rifletta i raggruppamenti di dominio (es. Attori in alto, Mobilità/Corse al centro, Pagamenti/Tariffe in basso, o secondo il raggruppamento più naturale per il progetto).

- Uso di colori di riempimento tenui e codificati per distinguere le diverse macro-aree del sistema.

- Non rinominare o inventare classi/attributi non presenti nel diagramma o nel backlog senza segnalarlo esplicitamente — la fonte di verità resta Diagramma Classi.drawio validato rispetto al backlog, non un'interpretazione libera.

### Diagrammi di Sequenza

Ruolo: Sei un Senior Software Engineer ed esperto di modellazione UML.

> Obiettivo: Generare un diagramma di sequenza UML accurato e dettagliato per uno specifico caso d'uso del sistema "SMART MOBILITY", garantendo la totale coerenza con i diagrammi architetturali già definiti.
>
> Input che ti fornirò a breve:
>
> 1\. La specifica testuale del caso d'uso (dalla documentazione dello Sprint 2).
>
> 2\. Un esempio di diagramma di sequenza in formato .drawio (analizza il codice XML di questo file per replicare la struttura, lo stile, le coordinate e le dimensioni dei nodi mxCell).
>
> 3\. Il diagramma delle classi e il diagramma delle componenti del sistema..
>
> Formato dell'Output: Genera il codice XML nativo e non compresso compatibile con draw.io (struttura mxfile -\> diagram -\> mxGraphModel -\> root -\> mxCell). Assicurati di assegnare ID univoci corretti (id, parent, source, target) e di collegare le frecce (messaggi) in modo ordinato lungo l'asse Y per rispettare la sequenza temporale. Restituisci l'output all'interno di un blocco di codice in modo che io possa salvarlo direttamente come file .drawio.
>
> Linee Guida per la Modellazione: Lifeline (Linee di vita): Identifica l'Attore (es. utente), le interfacce/View, i Controller, i Model e il Database. Mappa queste lifeline posizionandole correttamente sull'asse X per evitare sovrapposizioni.
>
> Chiamate e Metodi: Usa i nomi reali dei metodi e delle rotte presenti nel diagramma delle classi.
>
> Logica di Flusso: Crea le frecce per i messaggi sincroni/asincroni e le risposte tratteggiate. Gestisci correttamente i blocchi condizionali (come i fragment alt e opt in UML) se ci sono scenari alternativi o errori (es. validazione fallita).

Caso d'uso da analizzare: \[NOME CASO D’USO\]

> Conferma di aver compreso e chiedimi di fornirti gli input per iniziare. genera il file .drawio nella cartella Diagrammi/Diagrammi di Sequenza/\[nome\]

### Codifica

RUOLO

Sei un ingegnere del software senior del team Smart Mobility. Conosci a fondo l'architettura Client-Server + MVC del progetto e le sue regole definite nel file .claude/CLAUDE.md. Il tuo compito è produrre la codifica completa di un caso d'uso già specificato, in modo tracciabile, conforme ai diagrammi e testato.

OBIETTIVO

Implementa il caso d'uso \[ID, es. IF-OP.08\] — "\[nome esatto dell'item dal backlog\]".

FONTI DI VERITÀ (consultale prima di scrivere codice, in quest'ordine)

1.  Specifica del caso d'uso — file docs/Sprintn3.md (§ 1.4 backlog, più scenario base e scenari alternativi). Verifica sempre la corrispondenza nome–ID nel backlog. Non fidarti di ID trovati in commenti, nomi di file o altri diagrammi: vanno riverificati nel backlog.

2.  Diagramma di sequenza — file \[percorso. drawio\]. Definisce il flusso esatto delle chiamate tra i layer e i tipi di ritorno. È vincolante.

3.  Diagramma delle classi — file docs/Diagrammi/Diagramma Classi.drawio (export testuale: docs/Diagrammi/DiagrammaClassi.md). Definisce classi, attributi e relazioni. Non inventare classi o interfacce che non esistono qui. I nomi devono corrispondere esattamente.

4.  Diagramma delle componenti — file docs/Diagrammi/Diagramma Componenti.drawio (export: docs/Diagrammi/diagrammaComponenti.md). Definisce in quale componente o layer collocare ogni responsabilità.

PROCEDIMENTO (ragiona passo-passo prima di scrivere; mostra il ragionamento)

1.  Estrai dallo scenario base e dagli scenari alternativi: attore (UT/OP/AP), pre e post-condizioni, flusso principale, errori ed eccezioni.

2.  Dal diagramma di sequenza, elenca la catena di chiamate attesa: View → ApiService → Controller → BLL (Servizio…) → DAL (Repository…) → DB, con firme di metodo e tipi di ritorno.

3.  Verifica nel diagramma delle classi che ogni entità e metodo che intendi usare esista già. Se manca qualcosa di necessario, fermati e chiedi invece di inventarlo.

4.  Dal diagramma delle componenti, conferma in quale file di ogni layer va collocato il codice.

5.  Solo dopo, scrivi prima i test e poi l'implementazione.

VINCOLI ARCHITETTURALI (obbligatori — vedi CLAUDE.md)

• Controller: solo validazione HTTP e smistamento. Zero logica di business. • BLL (backend/bll/Servizio…): tutta la logica applicativa. Nessun accesso diretto al DB. • DAL (backend/dal/…Repository): solo accesso ai dati. Nessuna logica di business. • model/: ORM SQLAlchemy 2.0 puri (Mapped e mapped_column), con CheckConstraint in **table_args** e create_type=False sui SAEnum. Nessuna logica, nessun Pydantic.

• Frontend (frontend/src/services/…Service.ts e views/…): nessuna logica di business lato client.

• Lo stato del mezzo si modifica solo tramite ServizioMobilità, rispettando le transizioni valide.

• Usa sempre i termini del glossario (Corsa, Mezzo, Prenotazione, Zona, Segnalazione, ecc.): nomi di classi, metodi e variabili coerenti con il diagramma, non sinonimi.

• Rispetta i requisiti non funzionali pertinenti: IIN-2 sicurezza e ruoli, IIN-3 WCAG, IIN-4 estendibilità, IIN-5 portabilità.

TRACCIABILITÀ

Inserisci un commento di tracciabilità nel formato // \[ID\] azione (oppure \# \[ID\] azione in Python) solo nei punti architetturalmente rilevanti, dove il legame al requisito non è ovvio. Non ovunque.

TEST (Definition of Done)

• Almeno un test per lo scenario base e uno per ogni scenario alternativo documentato. • Test indipendenti dall'ordine di esecuzione. Per il comportamento persistente usa il DB di test (vedi conftest.py), non mock.

DOCUMENTAZIONE (parte della Definition of Done)

Aggiorna docs/Sprintn3.md con eventuali rifiniture allo scenario o al diagramma di sequenza.

OUTPUT ATTESO (in quest'ordine)

1.  Analisi: tabella dei layer coinvolti, con i file da creare o modificare e la corrispondenza metodo–ID.

2.  Discrepanze trovate (se presenti): annotale invece di assumere; per gli ID inesistenti nel backlog, segnalali in docs/CoerenzaDiagrammaClassi.md.

3.  Codice per ciascun layer, nell'ordine DAL → BLL → Controller → Service frontend → View, nei file corretti.

4.  Test.

5.  Checklist di auto-verifica (rispondi Sì o No con prova):

> • ID verificato in Sprintn3.md § 1.4
>
> • Flusso conforme al diagramma di sequenza
>
> • Nessuna classe o interfaccia inventata fuori dal diagramma delle classi
>
> • Responsabilità nel layer corretto (no logica in Controller o DAL)
>
> • Stato mezzo gestito solo da ServizioMobilità (se applicabile)
>
> • Termini del glossario rispettati
>
> • Test base e alternativi presenti e superati
>
> • Documentazione aggiornata

COSA NON FARE

• Non aggiungere funzionalità fuori dal Product Backlog.

• Non inventare classi o schemi non presenti nel diagramma delle classi: in caso di dubbio, chiedi.

• Non riusare un ID visto in un commento o nome di file senza riverificarlo nel backlog.

• Non committare codice non testato.

# Glossario

## Acronimi

- **AP**: Amministrazione Pubblica

- **API**: Application Programming Interface

- **BLL**: Business Logic Layer

- **CSV**: Comma-Separated Values

- **DAL**: Data Access Layer

- **DBMS**: Database Management System

- **NFC**: Near Field Communication

- **OP**: Operatore del Servizio

- **PDF**: Portable Document Format

- **UT**: Utente

- **HTTP**: HyperText Transfer Protocol

- **GPS**: Global Positioning System

- **GDPR**: General Data Protection Regulation

- **WCAG**: Web Content Accessibility Guidelines

- **MVC**: Model-View-Controller

- **CRUD**: Create, Read, Update, Delete

- **JWT**: JSON Web Token

## Definizioni

- **Account utente**: Insieme di credenziali, dati anagrafici, metodi di pagamento, e-mail, password e storico associati a un utente registrato. Il profilo personale è la vista utente dell'account.

- **Addebito**: Importo economico calcolato al termine di una corsa o di un evento tariffabile e prelevato dal metodo di pagamento associato all'account utente.

- **Amministrazione Pubblica:** Ente locale (comune o equivalente) che monitora l'andamento del servizio di sharing sul territorio e ne analizza i dati aggregati a supporto delle decisioni di pianificazione urbana. Nel sistema è un ruolo distinto da Utente e Operatore, privo di poteri di configurazione diretta della flotta o delle zone. Interagisce con il sistema tramite desktop.

- **Autonomia residua**: Valore numerico indicante la carica rimasta nella batteria di un mezzo elettrico (e-bike, e-scooter). Espresso in percentuale (%) o in chilometri stimati;

- **Corsa**: Sessione di utilizzo attivo di un mezzo sharing, che inizia con lo sblocco del veicolo e termina con la chiusura della sessione da parte dell'utente. Al termine viene calcolato e addebitato il costo. Sinonimo: Sessione.

- **Definisce Zona**: Il perimetro di una zona è valido solo se chiuso su almeno tre vertici distinti: lo strumento di disegno sulla mappa non permette di confermare un poligono aperto o con meno di tre vertici. Una zona non operativa (Vietata, Limitata, di Parcheggio) è inoltre valida solo se interamente contenuta in una Zona Operativa esistente; in caso contrario il sistema rifiuta la creazione e notifica l'operatore.

- **Dismissione (mezzo)**: Operazione con cui l'operatore rimuove definitivamente un mezzo dalla flotta, rendendolo non più disponibile per prenotazioni o corse. Non è consentita se il mezzo è impegnato in una missione attiva.

- **Fine corsa**: Evento che conclude una corsa; l'esito (valido, penalizzato, rifiutato) dipende dalla posizione del mezzo rispetto a Zona Operativa e Zona di parcheggio.

- **Formato Esportabile:** Formattazione offerta dalla piattaforma per l’esportazione dei dati. Include CSV, PDF.

- **Flotta**: Insieme di tutti i mezzi gestiti da un operatore nell'ambito del servizio di sharing su un determinato territorio.

- **Mappa Amministrazione Pubblica**: Visualizzazione cartografica accessibile all'Amministrazione Pubblica, che mostra l'area urbana di competenza con le zone definite (operativa, vietata, limitata, parcheggio) e layer statistici sovrapponibili — heatmap della distribuzione dei mezzi e intensità d'uso per zona. A supporto di decisioni di pianificazione e monitoraggio, non della gestione operativa della flotta.

- **Mappa Operatore**: Visualizzazione cartografica accessibile agli operatori del servizio, che mostra ogni 2 secondi la posizione e lo stato di tutti i mezzi della flotta, inclusi quelli nascosti alla Mappa Utente. Distinta dalla Mappa Utente per contenuto e permessi di accesso.

- **Mappa Utente**: Visualizzazione cartografica accessibile agli utenti, che mostra i mezzi disponibili con il relativo stato, le varie zone: vietata, limitata, parcheggio e confine operativo. Non mostra i mezzi rimossi dall'operatore.

- **Metodo di pagamento**: Strumento associato all'account utente (carta, wallet, ecc.) utilizzato per regolare gli addebiti.

- **Mezzo**: Qualsiasi veicolo messo a disposizione degli utenti nell'ambito del servizio: bicicletta a pedalata assistita (e-bike), monopattino elettrico (e-scooter) e macchina elettrica.

- **Mezzo disponibile:** Mezzo il cui stato (definito nel glossario) è Disponibile, ossia prenotabile da un utente. Gli unici visualizzabili nella Mappa Utente.

- **Offerta:** Politica commerciale definita e pubblicata dall'Operatore allo scopo di incentivare l'utilizzo del servizio. È caratterizzata da una denominazione, una data di scadenza, uno stato (attiva, scaduta o in bozza) e da un insieme di condizioni di applicazione. Si specializza nelle seguenti tipologie:

  - **Promozione**: riduce la tariffa standard o introduce condizioni agevolate (ad esempio parcheggi corretti o uno sconto percentuale).

  - **Abbonamento**: contratto a tempo determinato (mensile o annuale) che garantisce all'utente condizioni tariffarie agevolate o un numero di corse incluse.

- **Operatore del Servizio:** Soggetto (azienda privata o consorzio) responsabile della gestione operativa della flotta e della configurazione della piattaforma: definisce tariffe, promozioni, zone operative, zone soggette a restrizioni e zone di parcheggio parametri di prenotazione e pausa corsa. Interagisce con il sistema tramite desktop.

- **Parametri di sistema**: Insieme dei valori numerici configurabili che regolano il funzionamento operativo della piattaforma. Comprendono:

  - la durata massima di una prenotazione,

  - la durata del periodo di grazia per la pausa corsa,

  - il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente

  - l'importo di addebito al minuto applicato durante la pausa corsa al termine del periodo di grazia.

> *L'insieme dei parametri è aperto a future estensioni: nuovi parametri numerici operativi potranno essere aggiunti senza alterare la struttura del caso d'uso, in quanto condividono la stessa logica di configurazione, validazione e salvataggio.*

- **Pausa corsa**: Stato intermedio di una sessione in cui l'utente blocca temporaneamente il mezzo senza terminare la corsa.

- **Periodo di grazia**: Durata massima configurabile dall'operatore entro cui una pausa corsa non comporta addebiti aggiuntivi o la perdita del mezzo. Se impostato a zero, la funzionalità di pausa gratuita è disabilitata.

- **Prenotazione**: Operazione con cui un Utente riserva temporaneamente uno o più Mezzi disponibili per un utilizzo futuro. Il sistema verifica che i mezzi selezionati siano effettivamente disponibili e che il numero non superi il limite massimo di mezzi contemporanei per utente, definito nei Parametri di Sistema. In caso di **prenotazione di gruppo**, tutti i mezzi successivi al primo devono trovarsi entro un raggio limite dal primo selezionato (vincolo di prossimità del gruppo). Superati i controlli, lo stato di ciascun mezzo passa da Disponibile a Prenotato e viene creato un record di Prenotazione con una scadenza calcolata sulla base della durata massima configurata nei Parametri di Sistema. Se la prenotazione non viene convertita in Sblocco entro tale scadenza, viene automaticamente marcata come scaduta e il mezzo torna Disponibile. L'utente può in qualsiasi momento annullare una prenotazione attiva, riportando il mezzo a Disponibile.

- **Prenotazione di gruppo**: Prenotazione effettuata da un singolo utente per un numero di mezzi fino al massimo configurato dall'operatore (può anche essere uno).

- **ProviderMappa** — Attore secondario esterno (a livello di caso d'uso) che fornisce dati geografici e di geolocalizzazione al sistema (posizione utente, dati mappa, verifica zona). Nel diagramma delle classi è rappresentato concretamente dalla classe GoogleMaps, esposta tramite GoogleMapsAdapter per permettere la sostituzione del provider esterno senza modifiche strutturali al sistema.

- **Posizione di default**: Punto geografico su cui viene centrata la Mappa Utente quando la geolocalizzazione non è disponibile o l'utente nega il permesso di accesso alla posizione.

- **Recensione**: Valutazione espressa da un Utente a seguito di almeno una corsa effettuata, accessibile dalla voce "Lascia Recensione" nel menu principale. È composta da un voto numerico (da 1 a 5 stelle) e da un commento testuale facoltativo. Ha lo scopo di raccogliere feedback sull'esperienza d'uso del servizio. Un Utente può lasciare più recensioni nel tempo; non è vincolata a una singola corsa specifica.

- **Regole Fine Corsa**: Insieme di condizioni configurate dall'operatore che determinano l'esito del Fine Corsa. Comprendono: la penale applicata in caso di parcheggio fuori zona, il tipo di vincolo (penale, divieto, avviso) e l'eventuale Bonus riconosciuto all'utente per il parcheggio corretto. La definizione delle regole è separata dalla definizione geografica della Zona di parcheggio.

- **Redistribuzione**: Operazione logistica di spostamento fisico dei mezzi da aree con eccesso di offerta verso aree con carenza, eseguita dal personale operativo sulla base dei dati della Mappa Operatore.

- **Report aggregato**: Documento che consolida statistiche anonime sull'utilizzo del servizio (corse, km, fasce orarie, zone) su un intervallo temporale configurabile. Destinato all'amministrazione pubblica.

- **Riepilogo corsa**: Sintesi presentata all'utente al termine di una corsa, che riporta i dati principali della sessione: durata complessiva, distanza percorsa, costo finale calcolato sulla base della tariffa applicata ed eventuali sconti o bonus. Disponibile anche nello storico corse del profilo utente.

- **Sblocco**: Operazione con cui un Utente attiva uno o più Mezzi prenotati (o disponibili) per iniziare una Corsa. Il sistema verifica che l'utente si trovi entro un raggio limite dal mezzo: se la posizione dell'utente supera questa soglia, lo sblocco viene rifiutato. Superato il controllo di prossimità, il sistema verifica la disponibilità di ciascun mezzo e la sua posizione rispetto alle zone operative, crea una Corsa per ogni mezzo sbloccato e ne aggiorna lo stato da Prenotato (o Disponibile) a In uso. In caso di sblocco multiplo, tutte le corse generate condividono lo stesso gruppoCorsaId che le raggruppa come sessione unica. Lo sblocco è il passaggio che trasforma una prenotazione (o una selezione diretta) in un utilizzo effettivo del mezzo.

- **Segnalazione**: Comunicazione inviata dall'utente all'operatore per notificare anomalie su un mezzo (danno fisico, guasto, posizione anomala). Visibile nella Dashboard operatore. L’operatore aggiorna lo stato in “presa in carica” e “risolta” e all’utente viene mostrato tale cambiamento.

- **Sessione**: Sinonimo di Corsa. Periodo di utilizzo attivo di un mezzo, tracciato dal sistema con marcatura temporale di inizio e fine.

- **Sospensione account Utente**: Stato dell'account che ne disabilita l'accesso alle funzionalità della piattaforma, impostato dall'Operatore. Il tempo di sospensione è configurato dall’operatore: alla scadenza, l’account viene riattivato al primo accesso. Motivi tipici: danneggiamento ripetuto dei mezzi, uso fraudolento del servizio, violazioni ripetute delle Zone.

- **Stato (mezzo)**: Condizione operativa corrente di un mezzo. Valori possibili: Disponibile (prenotabile), Prenotato (riservato a un utente), In uso (corsa attiva), In pausa (pausa corsa attiva), In manutenzione (rimosso dalla Mappa Utente), Fuori servizio (bloccato o irrecuperabile), Dismesso.

- **Storico corsa**: L’insieme delle corse effettuate da un Utente.

- **Storico Modifiche:** Registro cronologico delle modifiche apportate dall'Operatore alle configurazioni del servizio, che consente di ricostruirne l'evoluzione nel tempo. Comprende le variazioni a: parametri numerici di sistema, regole di fine corsa, zone operative, tariffe e offerte. L'insieme delle configurazioni tracciate è aperto a future estensioni: il caso d'uso non cambia, cambia solo a livello implementativo quando una nuova categoria di configurazione viene aggiunta al registro.

- **Suggerimenti Intelligenti:** Insieme di indicazioni personalizzate prodotte da un servizio esterno di intelligenza artificiale (ServizioAI) a partire dai dati di utilizzo dell'Utente: storico corse, abitudini orarie, zone frequentate, prenotazioni effettuate, abbonamenti attivi e pagamenti. Il ServizioAI valuta autonomamente se i dati disponibili sono sufficienti a produrre indicazioni significative; in caso contrario non genera alcun suggerimento. I suggerimenti possono riguardare l'orario ottimale di prenotazione, la convenienza di un abbonamento rispetto alla tariffa ordinaria, o l'esistenza di promozioni compatibili con le abitudini dell'Utente. La generazione dei suggerimenti non modifica alcuno stato del sistema.

- **Tariffa**: Struttura di pricing applicata a una corsa. La tipologia (es. costo al minuto, alla distanza, tariffa fissa per fascia oraria) è definita e modificabile dall'operatore. La tariffa applicabile è mostrata all'utente prima dell'avvio della corsa.

- **Tariffario**: Elenco pubblicato dall'operatore delle tariffe applicate per ciascuna tipologia di mezzo e modalità di utilizzo. Distinto da Tariffa (struttura applicata alla singola corsa).

- **Utente:** Persona fisica registrata alla piattaforma che utilizza i mezzi di sharing per spostarsi nel contesto urbano. Interagisce con il sistema tramite dispositivo mobile.

- **Zona**:

  - **Zona Operativa**: Perimetro geografico definito dall'operatore entro cui i mezzi della flotta possono circolare e fermarsi. Un mezzo che esce dalla zona operativa riceve una notifica. La Zona Limitata e la Zona Vietata hanno sempre la precedenza sulla Zona Operativa.

  - **Zona di parcheggio**: Area geografica designata esclusivamente dall'operatore in cui è consigliato — ma non imposto — parcheggiare il mezzo al termine della corsa. Visibile sulla Mappa Utente. La definizione della zona riguarda esclusivamente il suo perimetro geografico; gli eventuali incentivi associati al parcheggio corretto sono configurati separatamente tramite le Regole Fine Corsa.

  - **Zona Soggetta a restrizioni:**

    - **Zona Limitata**: Area geografica in cui la circolazione dei mezzi è consentita ma con restrizioni configurabili (es. velocità ridotta, orari limitati, divieto di sosta o pausa). Configurata dall’Operatore.

    - **Zona Vietata**: Area geografica definita dall’Operatore in cui la circolazione dei mezzi è completamente vietata. Distinta dalla Zona Limitata (restrizioni parziali). Ha precedenza sulla Zona Operativa in caso di sovrapposizione.
