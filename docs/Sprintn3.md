**Ciclo 4**

**SMART MOBILITY**

Versione 2.0

Data di rilascio: 24/05/2026

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

[1.3 Stakeholder [11](#stakeholder)](#stakeholder)

[1.4 Item funzionali [12](#item-funzionali)](#item-funzionali)

[1.4.1 IF-UT.01 – Visualizza Mappa Utente [12](#if-ut.01-visualizza-mappa-utente)](#if-ut.01-visualizza-mappa-utente)

[1.4.2 IF-UT.02 – Prenota mezzo [12](#if-ut.02-prenota-mezzo)](#if-ut.02-prenota-mezzo)

[1.4.4 IF-UT.03 – Sblocca mezzo [12](#if-ut.03-sblocca-mezzo)](#if-ut.03-sblocca-mezzo)

[1.4.5 IF-UT.04 – Termina Corsa [12](#if-ut.04-termina-corsa)](#if-ut.04-termina-corsa)

[1.4.6 IF-UT.05 – Effettua Pagamento [12](#if-ut.05-effettua-pagamento)](#if-ut.05-effettua-pagamento)

[1.4.7 IF-UT.06 – Salva Metodi Pagamento [13](#if-ut.06-salva-metodi-pagamento)](#if-ut.06-salva-metodi-pagamento)

[1.4.8 IF-UT.07 – Consulta tariffe [13](#if-ut.07-consulta-tariffe)](#if-ut.07-consulta-tariffe)

[1.4.9 IF-UT.08 – Visualizza Riepilogo corsa [13](#if-ut.08-visualizza-riepilogo-corsa)](#if-ut.08-visualizza-riepilogo-corsa)

[1.4.10 IF-UT.09 – Sospende Corsa [13](#if-ut.09-sospende-corsa)](#if-ut.09-sospende-corsa)

[1.4.11 IF-UT.10 – Visualizza Promozioni [13](#if-ut.10-visualizza-promozioni)](#if-ut.10-visualizza-promozioni)

[1.4.12 IF-UT.11 – Visualizza Storico Corsa [13](#if-ut.11-visualizza-storico-corsa)](#if-ut.11-visualizza-storico-corsa)

[1.4.13 IF-UT.12 – Invia Segnalazione [14](#if-ut.12-invia-segnalazione)](#if-ut.12-invia-segnalazione)

[1.4.14 IF-UT.13 – Sottoscrive Abbonamento [14](#if-ut.13-sottoscrive-abbonamento)](#if-ut.13-sottoscrive-abbonamento)

[1.4.18 IF-AP.01 – Accede Report [14](#if-ut.15-scrive-una-recensione)](#if-ut.15-scrive-una-recensione)

[1.4.15 IF-AP.02 – Esporta Report [14](#if-ap.02-esporta-report)](#if-ap.02-esporta-report)

[1.4.16 IF-AP.03 – Visualizza Mappa Amministrazione Pubblica [14](#if-ap.03-visualizza-mappa-amministrazione-pubblica)](#if-ap.03-visualizza-mappa-amministrazione-pubblica)

[1.4.17 IF-OP.01 – Visualizza Mappa Operatore [14](#if-op.01-visualizza-mappa-operatore)](#if-op.01-visualizza-mappa-operatore)

[1.4.18 IF-OP.02 – Aggiunge Mezzo [15](#if-op.02-aggiunge-mezzo)](#if-op.02-aggiunge-mezzo)

[1.4.19 IF-OP.03 – Dismette Mezzo [15](#if-op.03-dismette-mezzo)](#if-op.03-dismette-mezzo)

[1.4.20 IF-OP.04 – Modifica Stato Mezzo [15](#if-op.04-modifica-stato-mezzo)](#if-op.04-modifica-stato-mezzo)

[1.4.21 IF-OP.05 – Definisce Tariffa [15](#if-op.05-definisce-tariffa)](#if-op.05-definisce-tariffa)

[1.4.22 IF-OP.06 – Definisce Regole Fine Corsa [15](#if-op.06-definisce-regole-fine-corsa)](#if-op.06-definisce-regole-fine-corsa)

[1.4.23 IF-OP.07 - Definisce Zone [15](#if-op.07---definisce-zone)](#if-op.07---definisce-zone)

[1.4.24 IF-OP.08 – Gestisce Segnalazioni [16](#if-op.08-gestisce-segnalazioni)](#if-op.08-gestisce-segnalazioni)

[1.4.25 IF-OP.09– Sospende Account Utente [16](#if-op.09-sospende-account-utente)](#if-op.09-sospende-account-utente)

[1.4.26 IF-OP.10– Definisce Offerte [16](#if-op.10-definisce-offerte)](#if-op.10-definisce-offerte)

[1.4.27 IF-OP.11 – Configura Parametri Sistema [16](#if-op.11-configura-parametri-sistema)](#if-op.11-configura-parametri-sistema)

[1.5 Item non funzionali [16](#item-non-funzionali)](#item-non-funzionali)

[1.5.1 Item Informativi [16](#item-informativi)](#item-informativi)

[1.5.1.1 IIN-1 Prestazioni [16](#iin-1-prestazioni)](#iin-1-prestazioni)

[1.5.1.2 IIN-2 Sicurezza [17](#iin-2-sicurezza)](#iin-2-sicurezza)

[1.5.1.3 IIN-3 Usabilità [17](#iin-3-usabilità)](#iin-3-usabilità)

[1.5.1.4 IIN-4 Scalabilità [17](#iin-4-scalabilità)](#iin-4-scalabilità)

[1.5.1.5 IIN-5 Portabilità [17](#iin-5-portabilità)](#iin-5-portabilità)

[1.5.1.6 Conformità [17](#conformità)](#conformità)

[1.5.2 Item di interfaccia [17](#item-di-interfaccia)](#item-di-interfaccia)

[1.5.2.1 IUI-1 - Schermata di Login Utente [18](#iui-1---schermata-di-login-utente)](#iui-1---schermata-di-login-utente)

[1.5.2.2 IUI-2 – Homepage Utente [18](#map-screenshot-showing-a-section-of-bari-italy-with-colored-markers-indicating-different-transportation-options-around-politecnico-di-bari-and-università-degli-studi-di-bari.-blue-markers-represent-bicycles-green-markers-indicate-scooters-and-purple-markers-show-cars-with-a-red-shaded-area-highlighting-politecnico-di-bari-and-a-red-location-pin-marking-a-specific-point-nearby.iui-2-homepage-utente)](#map-screenshot-showing-a-section-of-bari-italy-with-colored-markers-indicating-different-transportation-options-around-politecnico-di-bari-and-università-degli-studi-di-bari.-blue-markers-represent-bicycles-green-markers-indicate-scooters-and-purple-markers-show-cars-with-a-red-shaded-area-highlighting-politecnico-di-bari-and-a-red-location-pin-marking-a-specific-point-nearby.iui-2-homepage-utente)

[1.5.2.3 IUI-3 – Menu Laterale Utente [18](#screenshot-of-a-mobile-app-menu-for-a-smart-mobility-service-displaying-options-in-italian-such-as-profile-pricing-plan-bonuses-and-promotions-history-settings-wallet-and-guide-with-corresponding-icons.-the-menu-overlays-a-partial-map-showing-bike-icons-near-via-giuseppe-re-indicating-bike-sharing-locations.iui-3-menu-laterale-utente)](#screenshot-of-a-mobile-app-menu-for-a-smart-mobility-service-displaying-options-in-italian-such-as-profile-pricing-plan-bonuses-and-promotions-history-settings-wallet-and-guide-with-corresponding-icons.-the-menu-overlays-a-partial-map-showing-bike-icons-near-via-giuseppe-re-indicating-bike-sharing-locations.iui-3-menu-laterale-utente)

[1.5.2.4 IUI-4 – Corsa di Gruppo [19](#iui-4-corsa-di-gruppo)](#iui-4-corsa-di-gruppo)

[1.5.2.5 IUI-5 – Prenotazione Mezzo [19](#screenshot-of-a-scooter-rental-app-interface-showing-a-map-with-a-green-location-pin-indicating-scooter-availability-near-politecnico-di-bari.-the-booking-panel-displays-scooter-id-bz234vf-a-full-battery-icon-and-a-countdown-timer-until-1647-to-unlock-the-scooter-with-a-green-prenota-button-for-reservation.iui-5-prenotazione-mezzo)](#screenshot-of-a-scooter-rental-app-interface-showing-a-map-with-a-green-location-pin-indicating-scooter-availability-near-politecnico-di-bari.-the-booking-panel-displays-scooter-id-bz234vf-a-full-battery-icon-and-a-countdown-timer-until-1647-to-unlock-the-scooter-with-a-green-prenota-button-for-reservation.iui-5-prenotazione-mezzo)

[1.5.2.6 IUI-6 – Visualizzazione del Piano Tariffario [20](#screenshot-of-a-tariff-pricing-chart-for-different-transportation-modes-showing-costs-per-kilometer-for-electric-scooter-0.20km-bicycle-0.30km-and-automobile-0.50km.-the-chart-uses-black-icons-for-each-vehicle-type-alongside-green-text-for-labels-and-prices-with-a-smart-mobility-logo-below-and-navigation-icons-at-the-bottom.iui-6-visualizzazione-del-piano-tariffario)](#screenshot-of-a-tariff-pricing-chart-for-different-transportation-modes-showing-costs-per-kilometer-for-electric-scooter-0.20km-bicycle-0.30km-and-automobile-0.50km.-the-chart-uses-black-icons-for-each-vehicle-type-alongside-green-text-for-labels-and-prices-with-a-smart-mobility-logo-below-and-navigation-icons-at-the-bottom.iui-6-visualizzazione-del-piano-tariffario)

[1.5.2.7 IUI-7 – Visualizzazione del Saldo e Metodi di Pagamento [20](#screenshot-of-a-digital-wallet-interface-showing-a-zero-balance-with-payment-method-options-including-google-pay-apple-pay-paypal-and-credit-card-addition.-the-layout-features-green-text-and-buttons-with-icons-for-each-payment-method-and-a-prominent-green-button-labeled-ricarica-saldo-for-recharging-balance.iui-7-visualizzazione-del-saldo-e-metodi-di-pagamento)](#screenshot-of-a-digital-wallet-interface-showing-a-zero-balance-with-payment-method-options-including-google-pay-apple-pay-paypal-and-credit-card-addition.-the-layout-features-green-text-and-buttons-with-icons-for-each-payment-method-and-a-prominent-green-button-labeled-ricarica-saldo-for-recharging-balance.iui-7-visualizzazione-del-saldo-e-metodi-di-pagamento)

[1.5.2.8 IUI-8 – Schermata Info Corsa [21](#screenshot-of-a-scooter-rental-app-interface-displaying-trip-information.-it-shows-scooter-id-bz234vf-remaining-battery-level-elapsed-time-of-46-seconds-and-distance-traveled-of-0.3-kilometers-with-buttons-to-end-and-pay-or-pause-the-ride.iui-8-schermata-info-corsa)](#screenshot-of-a-scooter-rental-app-interface-displaying-trip-information.-it-shows-scooter-id-bz234vf-remaining-battery-level-elapsed-time-of-46-seconds-and-distance-traveled-of-0.3-kilometers-with-buttons-to-end-and-pay-or-pause-the-ride.iui-8-schermata-info-corsa)

[1.5.2.9 IUI-9 – Visualizzazione della Cronologia Corse [21](#screenshot-of-a-transportation-log-displaying-four-entries-with-icons-for-electric-scooter-bicycle-car-and-another-electric-scooter.-each-entry-includes-id-bz345tr-elapsed-time-1021-distance-traveled-4.98-km-and-date-04052026-with-teal-text-and-icons-on-a-white-background.iui-9-visualizzazione-della-cronologia-corse)](#screenshot-of-a-transportation-log-displaying-four-entries-with-icons-for-electric-scooter-bicycle-car-and-another-electric-scooter.-each-entry-includes-id-bz345tr-elapsed-time-1021-distance-traveled-4.98-km-and-date-04052026-with-teal-text-and-icons-on-a-white-background.iui-9-visualizzazione-della-cronologia-corse)

[1.5.2.10 IUI-10 – Schermata Login Operatore/Amministrazione Pubblica [21](#iui-10-schermata-login-operatoreamministrazione-pubblica)](#iui-10-schermata-login-operatoreamministrazione-pubblica)

[1.5.2.11 IUI-11 – Dashboard Amministrazione Pubblica [22](#iui-11-dashboard-amministrazione-pubblica)](#iui-11-dashboard-amministrazione-pubblica)

[1.5.2.12 IUI-12 – Definizione Zone Vietate [22](#map-showing-a-restricted-zone-in-bari-outlined-by-red-points-indicating-areas-where-certain-vehicles-cannot-enter.-the-right-panel-lists-vehicle-types-with-a-green-checkmark-on-automobile-highlighting-that-cars-are-prohibited-from-the-red-zone-while-scooters-and-bicycles-are-not-restricted.iui-12-definizione-zone-vietate)](#map-showing-a-restricted-zone-in-bari-outlined-by-red-points-indicating-areas-where-certain-vehicles-cannot-enter.-the-right-panel-lists-vehicle-types-with-a-green-checkmark-on-automobile-highlighting-that-cars-are-prohibited-from-the-red-zone-while-scooters-and-bicycles-are-not-restricted.iui-12-definizione-zone-vietate)

[1.5.2.13 IUI-13 – Definizione Zone Limitate [23](#iui-13-definizione-zone-limitate)](#iui-13-definizione-zone-limitate)

[1.5.2.14 IUI-14 – Definizione Zone di Parcheggio [23](#iui-14-definizione-zone-di-parcheggio)](#iui-14-definizione-zone-di-parcheggio)

[1.5.2.15 IUI-15 – Visualizzazione dei Report [23](#bar-chart-and-pie-chart-displaying-weekly-and-overall-distribution-of-three-categories-monopattini-green-automobili-pink-and-biciclette-blue.-bar-chart-shows-daily-counts-with-monopattini-highest-on-monday-and-decreasing-through-the-week-while-pie-chart-highlights-monopattini-as-majority-at-55.8-followed-by-biciclette-at-31.3-and-automobili-at-11.4.iui-15-visualizzazione-dei-report)](#bar-chart-and-pie-chart-displaying-weekly-and-overall-distribution-of-three-categories-monopattini-green-automobili-pink-and-biciclette-blue.-bar-chart-shows-daily-counts-with-monopattini-highest-on-monday-and-decreasing-through-the-week-while-pie-chart-highlights-monopattini-as-majority-at-55.8-followed-by-biciclette-at-31.3-and-automobili-at-11.4.iui-15-visualizzazione-dei-report)

[1.5.2.16 IUI-16 – Dashboard Operatore [24](#iui-16-dashboard-operatore)](#iui-16-dashboard-operatore)

[1.5.2.17 IUI-17 – Gestione Segnalazioni [24](#iui-17-gestione-segnalazioni)](#iui-17-gestione-segnalazioni)

[1.5.2.18 IUI-18 – Gestione Tariffe e Promozioni [24](#iui-18-gestione-tariffe-e-promozioni)](#iui-18-gestione-tariffe-e-promozioni)

[1.5.2.19 IUI-19 – Schermata di Impostazione Regole [25](#screenshot-of-a-settings-panel-titled-impostazioni-regole-displaying-configurable-rules-for-booking-and-business-operations.-it-includes-fields-with-numerical-values-for-maximum-booking-duration-30-min-grace-period-for-pause-10-min-maximum-concurrent-bookings-per-user-5-tariff-percentage-during-pause-100-and-a-dropdown-menu-with-options-related-to-business-rules-outside-parking-zones.iui-19-schermata-di-impostazione-regole)](#screenshot-of-a-settings-panel-titled-impostazioni-regole-displaying-configurable-rules-for-booking-and-business-operations.-it-includes-fields-with-numerical-values-for-maximum-booking-duration-30-min-grace-period-for-pause-10-min-maximum-concurrent-bookings-per-user-5-tariff-percentage-during-pause-100-and-a-dropdown-menu-with-options-related-to-business-rules-outside-parking-zones.iui-19-schermata-di-impostazione-regole)

[1.5.3 Item Qualitativi [25](#item-qualitativi)](#item-qualitativi)

[1.5.3.1 IQ-1 [25](#iq-1)](#iq-1)

[1.5.3.2 IQ-2 [25](#iq-2)](#iq-2)

[1.5.3.3 IQ-n [25](#iq-n)](#iq-n)

[1.5.4 Altri Item [25](#altri-item)](#altri-item)

[2. Sprint Report [27](#sprint-report)](#sprint-report)

[2.1 Sprint Backlog [27](#sprint-backlog)](#sprint-backlog)

[2.2 Product Requirement Specification [29](#product-requirement-specification)](#product-requirement-specification)

[2.2.1 Diagramma dei Casi d’uso [29](#diagramma-dei-casi-duso)](#diagramma-dei-casi-duso)

[2.2.2 Specifiche dei Casi d’uso [30](#specifiche-dei-casi-duso)](#specifiche-dei-casi-duso)

[2.2.2.1 UT – 01 Visualizza Mappa utente [30](#ut-01-visualizza-mappa-utente)](#ut-01-visualizza-mappa-utente)

[2.2.2.2 UT – 02 Prenota Mezzo [30](#ut-02-prenota-mezzo)](#ut-02-prenota-mezzo)

[2.2.2.3 UT – 03 Sblocca Mezzo [33](#ut-03-sblocca-mezzo)](#ut-03-sblocca-mezzo)

[2.2.2.4 UT – 04 Termina corsa [34](#ut-04-termina-corsa)](#ut-04-termina-corsa)

[2.2.2.5 UT – 05 Effettua Pagamento [36](#ut-05-effettua-pagamento)](#ut-05-effettua-pagamento)

[2.2.2.6 UT - 06 Salva Metodo di Pagamento [37](#ut---06-salva-metodo-di-pagamento)](#ut---06-salva-metodo-di-pagamento)

[2.2.2.1 UT – 07 Consulta Tariffe [39](#ut-07-consulta-tariffe)](#ut-07-consulta-tariffe)

[2.2.2.2 UT – 08 Visualizza Riepilogo Corsa [40](#ut-08-visualizza-riepilogo-corsa)](#ut-08-visualizza-riepilogo-corsa)

[2.2.2.3 UT – 09 Sospende Corsa [41](#ut-09-sospende-corsa)](#ut-09-sospende-corsa)

[2.2.2.4 UT – 10 Visualizza Promozioni [43](#ut-10-visualizza-promozioni)](#ut-10-visualizza-promozioni)

[2.2.2.5 UT – 11 Visualizza Storico Corse [44](#ut-11-visualizza-storico-corse)](#ut-11-visualizza-storico-corse)

[2.2.2.6 UT – 12 Invia Segnalazione [45](#ut-12-invia-segnalazione)](#ut-12-invia-segnalazione)

[2.2.2.7 UT – 13 Sottoscrive Abbonamento [46](#ut-13-sottoscrive-abbonamento)](#ut-13-sottoscrive-abbonamento)

[2.2.2.8 AP – 01 Accede Report [47](#ap-01-accede-report)](#ap-01-accede-report)

[2.2.2.9 AP - 02 Esporta Report [49](#ap---02-esporta-report)](#ap---02-esporta-report)

[2.2.2.10 AP – 03 Visualizza Mappa Amministrazione Pubblica [51](#ap-03-visualizza-mappa-amministrazione-pubblica)](#ap-03-visualizza-mappa-amministrazione-pubblica)

[2.2.2.11 OP – 01 Visualizza Mappa Operatore [53](#op-01-visualizza-mappa-operatore)](#op-01-visualizza-mappa-operatore)

[2.2.2.12 OP – 02 Aggiunge Mezzo [54](#op-02-aggiunge-mezzo)](#op-02-aggiunge-mezzo)

[2.2.2.13 OP – 03 Dismette Mezzo [55](#op-03-dismette-mezzo)](#op-03-dismette-mezzo)

[2.2.2.14 OP – 04 Modifica stato mezzo [57](#op-04-modifica-stato-mezzo)](#op-04-modifica-stato-mezzo)

[2.2.2.15 OP – 05 Definisce tariffa [58](#op-05-definisce-tariffa)](#op-05-definisce-tariffa)

[2.2.2.16 OP-06 Definisce Regole Fine Corsa [59](#op-06-definisce-regole-fine-corsa)](#op-06-definisce-regole-fine-corsa)

[2.2.2.17 OP-07 Definisce Zona [61](#op-07-definisce-zona)](#op-07-definisce-zona)

[2.2.2.18 OP-08 Gestisce Segnalazione [62](#op-08-gestisce-segnalazione)](#op-08-gestisce-segnalazione)

[2.2.2.19 OP-09 Sospende Account Utente [63](#op-09-sospende-account-utente)](#op-09-sospende-account-utente)

[2.2.2.20 OP-10 Definisce Offerta [64](#op-10-definisce-offerta)](#op-10-definisce-offerta)

[2.2.2.21 OP-11 Configura parametri di sistema [65](#op-11-configura-parametri-di-sistema)](#op-11-configura-parametri-di-sistema)

[2.3 System Architecture [68](#system-architecture)](#system-architecture)

[2.3.1 Diagramma delle Componenti – Diagramma Generale [68](#diagramma-delle-componenti-diagramma-generale)](#diagramma-delle-componenti-diagramma-generale)

[2.3.1.1 Client [69](#client)](#client)

[2.3.1.2 Server [70](#server)](#server)

[2.3.2 Specifica delle componenti [70](#specifica-delle-componenti)](#specifica-delle-componenti)

[2.3.2.1 Specifica delle componenti client [70](#specifica-delle-componenti-client)](#specifica-delle-componenti-client)

[2.3.2.2 Specifica delle componenti server [73](#specifica-delle-componenti-server)](#specifica-delle-componenti-server)

[2.3.2.3 Specifica delle componenti Servizi Esterni [76](#specifica-delle-componenti-servizi-esterni)](#specifica-delle-componenti-servizi-esterni)

[2.3.2.4 Specifica delle componenti Persistenza [76](#specifica-delle-componenti-persistenza)](#specifica-delle-componenti-persistenza)

[2.4 Detailed Product Design [77](#detailed-product-design)](#detailed-product-design)

[2.4.1 Diagramma delle Classi – Diagramma Generale [77](#diagramma-delle-classi-diagramma-generale)](#diagramma-delle-classi-diagramma-generale)

[2.4.1.1 Diagramma delle Classi – Client [78](#diagramma-delle-classi-client)](#diagramma-delle-classi-client)

[2.4.1.2 Diagramma delle Classi – Server [79](#diagramma-delle-classi-server)](#diagramma-delle-classi-server)

[2.4.1.3 Diagramma delle Classi – View [80](#diagramma-delle-classi-view)](#diagramma-delle-classi-view)

[2.4.1.4 Diagramma delle Classi – APIService [81](#diagramma-delle-classi-apiservice)](#diagramma-delle-classi-apiservice)

[2.4.1.5 Diagramma delle Classi – interfacce Client/Server [82](#diagramma-delle-classi-interfacce-clientserver)](#diagramma-delle-classi-interfacce-clientserver)

[2.4.1.6 Diagramma delle Classi – Controller [83](#diagramma-delle-classi-controller)](#diagramma-delle-classi-controller)

[2.4.1.7 Diagramma delle Classi – Business Logic Layer [83](#diagramma-delle-classi-business-logic-layer)](#diagramma-delle-classi-business-logic-layer)

[2.4.1.8 Diagramma delle Classi – Model [84](#diagramma-delle-classi-model)](#diagramma-delle-classi-model)

[2.4.1.9 Diagramma delle Classi – Data Access Layer [85](#diagramma-delle-classi-data-access-layer)](#diagramma-delle-classi-data-access-layer)

[2.4.2 Specifiche delle Classi [86](#specifiche-delle-classi)](#specifiche-delle-classi)

[2.4.2.1 Specifica delle Classi – Client [86](#specifica-delle-classi-client)](#specifica-delle-classi-client)

[2.4.2.1.1 Panoramica architetturale [86](#panoramica-architetturale)](#panoramica-architetturale)

[2.4.2.1.2 Interfacce [86](#interfacce)](#interfacce)

[2.4.2.1.3 Livello API Service [87](#livello-api-service)](#livello-api-service)

[2.4.2.1.4 Livello View [89](#livello-view)](#livello-view)

[2.4.2.1.4.1 UTENTE [89](#utente)](#utente)

[2.4.2.1.4.2 Amministratore Pubblica [89](#amministratore-pubblica)](#amministratore-pubblica)

[2.4.2.1.4.3 Operatore [89](#operatore)](#operatore)

[2.4.2.1.5 Relazioni tra le classi [90](#relazioni-tra-le-classi)](#relazioni-tra-le-classi)

[2.4.2.2 Specifica delle Classi – Server [91](#specifica-delle-classi-server)](#specifica-delle-classi-server)

[2.4.2.2.1 Panoramica architetturale [91](#panoramica-architetturale-1)](#panoramica-architetturale-1)

[2.4.2.2.2 Interfacce [92](#interfacce-1)](#interfacce-1)

[2.4.2.2.3 Livello Controller [93](#livello-controller)](#livello-controller)

[2.4.2.2.4 Livello Business Logic Layer [94](#livello-business-logic-layer)](#livello-business-logic-layer)

[2.4.2.2.5 Livello Model [96](#livello-model)](#livello-model)

[2.4.2.2.6 Livello Data Access Layer [97](#livello-data-access-layer)](#livello-data-access-layer)

[2.4.2.2.7 Relazioni tra le classi [99](#relazioni-tra-le-classi-1)](#relazioni-tra-le-classi-1)

[2.4.3 Diagrammi di Sequenza [100](#diagrammi-di-sequenza)](#diagrammi-di-sequenza)

[2.4.3.1 UT - 01 Visualizza Mappa Utente [100](#ut---01-visualizza-mappa-utente)](#ut---01-visualizza-mappa-utente)

[2.4.3.2 UT - 02 Prenota Mezzo [101](#ut---02-prenota-mezzo)](#ut---02-prenota-mezzo)

[2.4.3.3 UT – 03 Sblocca Mezzo [102](#ut-03-sblocca-mezzo-1)](#ut-03-sblocca-mezzo-1)

[2.4.3.4 UT – 04 Termina Corsa [103](#ut-04-termina-corsa-1)](#ut-04-termina-corsa-1)

[2.4.3.5 UT – 05 Effettua Pagamento [104](#ut-05-effettua-pagamento-1)](#ut-05-effettua-pagamento-1)

[2.4.3.6 UT – 06 Salva Metodo di Pagamento [105](#ut-06-salva-metodo-di-pagamento)](#ut-06-salva-metodo-di-pagamento)

[2.4.3.7 UT – 07 Consulta Tariffe [106](#ut-07-consulta-tariffe-1)](#ut-07-consulta-tariffe-1)

[2.4.3.8 UT – 08 Visualizza Riepilogo Corsa [107](#ut-08-visualizza-riepilogo-corsa-1)](#ut-08-visualizza-riepilogo-corsa-1)

[2.4.3.9 UT - 09 Sospende Corsa [108](#ut---09-sospende-corsa)](#ut---09-sospende-corsa)

[2.4.3.10 UT – 10 Visualizza Promozioni [109](#ut-10-visualizza-promozioni-1)](#ut-10-visualizza-promozioni-1)

[2.4.3.11 UT – 11 Visualizza Storico Corsa [110](#ut-11-visualizza-storico-corsa)](#ut-11-visualizza-storico-corsa)

[2.4.3.12 UT – 12 Invia Segnalazione [111](#ut-12-invia-segnalazione-1)](#ut-12-invia-segnalazione-1)

[2.4.3.13 UT – 13 Sottoscrive Abbonamento [112](#ut-13-sottoscrive-abbonamento-1)](#ut-13-sottoscrive-abbonamento-1)

[2.4.3.14 AP – 01 Accede Report [113](#ap-01-accede-report-1)](#ap-01-accede-report-1)

[2.4.3.15 AP – 02 Esporta Report [114](#ap-02-esporta-report)](#ap-02-esporta-report)

[2.4.3.16 AP – 03 Visualizza Mappa Amministrazione Pubblica [115](#ap-03-visualizza-mappa-amministrazione-pubblica-1)](#ap-03-visualizza-mappa-amministrazione-pubblica-1)

[2.4.3.17 OP-01 Visualizza Mappa Operatore [115](#op-01-visualizza-mappa-operatore-1)](#op-01-visualizza-mappa-operatore-1)

[2.4.3.18 OP – 02 Aggiunge Mezzo [116](#op-02-aggiunge-mezzo-1)](#op-02-aggiunge-mezzo-1)

[2.4.3.19 OP – 03 Dismette Mezzo [116](#op-03-dismette-mezzo-1)](#op-03-dismette-mezzo-1)

[2.4.3.20 OP – 04 Modifica Stato Mezzo [117](#op-04-modifica-stato-mezzo-1)](#op-04-modifica-stato-mezzo-1)

[2.4.3.21 OP – 05 Definisce Tariffa [118](#op-05-definisce-tariffa-1)](#op-05-definisce-tariffa-1)

[2.4.3.22 OP – 06 Definisce Regole fine corsa [119](#op-06-definisce-regole-fine-corsa-1)](#op-06-definisce-regole-fine-corsa-1)

[2.4.3.23 OP – 07 Definisce Zona [120](#op-07-definisce-zona-1)](#op-07-definisce-zona-1)

[2.4.3.24 OP – 08 Gestisce Segnalazione [121](#op-08-gestisce-segnalazione-1)](#op-08-gestisce-segnalazione-1)

[2.4.3.25 OP – 09 Sospende account utente [122](#op-09-sospende-account-utente-1)](#op-09-sospende-account-utente-1)

[2.4.3.26 OP – 10 Definisce Offerta [123](#op-10-definisce-offerta-1)](#op-10-definisce-offerta-1)

[2.4.3.27 OP – 11 Configura parametri numerici di sistema [124](#op-11-configura-parametri-numerici-sistema)](#op-11-configura-parametri-numerici-sistema)

[2.5 Data modeling and design [124](#data-modeling-and-design)](#data-modeling-and-design)

[2.5.1 Modello logico del Database [125](#modello-logico-del-database)](#modello-logico-del-database)

[2.5.2 Struttura fisica del Database [125](#struttura-fisica-del-database)](#struttura-fisica-del-database)

[3. Prompt [126](#prompt)](#prompt)

[3.1 Qualità dei requisiti [126](#qualità-dei-requisiti)](#qualità-dei-requisiti)

[3.2 Output Prompt Requisiti [134](#_Toc231754872)](#_Toc231754872)

[3.3 Definizioni [135](#_Toc231754873)](#_Toc231754873)

[4. Glossario [136](#glossario)](#glossario)

[4.1 Acronimi [136](#acronimi)](#acronimi)

[4.2 Definizioni [136](#definizioni)](#definizioni)

Product Backlog

**CICLO 4**

**SMART MOBILITY**

# Product Backlog

## Introduzione 

SMART MOBILITY è un sistema software progettato per supportare il Comune di Zootropolis nell'introduzione di un servizio integrato di mobilità urbana sostenibile, che mette a fattor comune diversi servizi di sharing (bike sharing, car sharing, e-scooter sharing e altri) in un'unica piattaforma accessibile a cittadini, operatori e amministrazione pubblica.

Il Sistema si pone tre obiettivi macroscopici:

- Offrire ai cittadini un accesso rapido, sicuro e trasparente ai mezzi di sharing disponibili sul territorio

- Permettere agli operatori del servizio di gestire in modo efficiente la flotta, ridurre costi e fenomeni di vandalismo

- Consentire all'Amministrazione Pubblica di monitorare la mobilità urbana e assumere decisioni strategiche basate su dati

Tali obiettivi si traducono in un insieme di funzionalità che coprono l'intero ciclo di utilizzo del servizio per soddisfare le esigenze delle tre categorie di utenti destinatari del sistema SMART MOBILITY — Utenti finali, Operatori del Servizio e Amministrazione Pubblica.

Per quanto riguarda gli Utenti, SMART MOBILITY offre:

- Visualizzazione dei mezzi disponibili nelle vicinanze e del loro stato

- Prenotazione di uno o più mezzi e sblocco tramite dispositivo personale

- Pagamenti veloci e sicuri

- Garanzia di affidabilità del sistema, con meccanismi di prevenzione di frodi ed errori

- Promozioni, pausa della corsa e gestione del profilo di pagamento

Per quanto riguarda gli Operatori del Servizio, SMART MOBILITY offre:

- Visualizzazione della distribuzione della flotta e notifiche sulle aree con bassa disponibilità, per ottimizzare la redistribuzione dei mezzi sul territorio

- Monitoraggio di malfunzionamenti, manutenzione pianificata e posizione dei mezzi a fine corsa, per ridurre i costi operativi e contenere i fenomeni di furto e vandalismo

- Bonus per parcheggio corretto, sospensione account in caso di frode e blocco automatico dei mezzi fuori dalle zone consentite

- Selezione di zone sensibili con divieto o limitazione del transito e definizione delle zone di parcheggio e del confine operativo

Per quanto riguarda l'Amministrazione Pubblica, SMART MOBILITY offre:

- Monitoraggio della frequenza di utilizzo delle diverse tipologie di mezzo e dei pattern di mobilità urbana, a supporto delle decisioni strategiche di pianificazione

- Accesso a report aggregati per supportare decisioni strategiche sulla mobilità

- Analisi dello stato dei mezzi e delle tratte più utilizzate per pianificare manutenzioni e interventi urbani, contribuendo alla garanzia della sicurezza urbana

- Visualizzazione cartografica del territorio operativo per il monitoraggio del servizio sulla città

## Contesto di business

Nel panorama urbano contemporaneo, caratterizzato da un'emergenza climatica sempre più pressante, dalla necessità di decongestionare i centri storici e dalla transizione verso modelli di "Smart City", emerge con forza l'esigenza di soluzioni integrate per la mobilità dolce e condivisa. SMART Mobility nasce per rispondere a questa sfida, superando la frammentazione degli attuali servizi di sharing e offrendo una piattaforma unica che connette cittadini, operatori privati e pubblica amministrazione. Il software è pensato per essere usato nei seguenti ambiti:

- **Contesto di mobilità per i cittadini:** in un ambiente urbano dove possedere un mezzo privato è sempre più costoso e inefficiente, i cittadini necessitano di strumenti che permettano di pianificare spostamenti intermodali in tempo reale. SMART Mobility offre un ecosistema che permette all'utente di localizzare, prenotare e pagare diversi tipi di mezzi (bici, monopattini, auto elettriche) tramite un'unica interfaccia, garantendo trasparenza sulle tariffe e sulla disponibilità, oltre a incentivare comportamenti virtuosi tramite bonus per il parcheggio corretto.

- **Contesto operativo degli operatori di flotta:** la gestione di una flotta di mezzi condivisi comporta sfide logistiche enormi, dal recupero dei mezzi scarichi alla manutenzione per atti vandalici. Gli operatori necessitano di strumenti avanzati per il monitoraggio costante della flotta, la gestione delle zone operative e l'ottimizzazione dei flussi di ridistribuzione. A questo scopo SMART Mobility mette a disposizione una "dashboard di controllo" che consente agli operatori di definire le zone vietate, le zone a circolazione limitata, le aree di parcheggio e il confine operativo della flotta, regolando in tempo reale la circolazione dei mezzi sul territorio. Il sistema permette inoltre ai gestori di massimizzare il tempo di attività dei mezzi, ridurre i costi di recupero e analizzare le zone a maggior rendimento.

- **Contesto di governance dell'Amministrazione Pubblica:** i comuni si trovano spesso a subire l'invasione di mezzi di sharing senza avere gli strumenti per monitorarli efficacemente. SMART Mobility offre alle amministrazioni una dashboard di monitoraggio che consente di osservare in tempo reale la distribuzione dei mezzi e lo stato del servizio sul territorio. Il sistema consente di raccogliere dati granulari sui flussi di traffico e di accedere a report aggregati, permettendo di pianificare infrastrutture ciclabili e pedonali basandosi su evidenze reali anziché su stime.

- **Contesto di sostenibilità e monitoraggio ambientale:** in un'epoca di obiettivi stringenti per la riduzione della CO2, cresce il bisogno di monitorare l'impatto ambientale dei trasporti. SMART Mobility risponde a questa esigenza fornendo statistiche aggregate sui chilometri percorsi con mezzi elettrici e sul risparmio di emissioni, permettendo sia all'utente che al Comune di visualizzare il proprio contributo concreto alla transizione ecologica.

In questo scenario, SMART Mobility si propone come piattaforma integrata che supera i limiti dei singoli servizi proprietari, offrendo un'esperienza fluida e centralizzata che risponde alle esigenze di tutti gli attori della mobilità urbana.

## Stakeholder

Il sistema SMART Mobility coinvolge diversi stakeholder che interagiscono con la piattaforma con ruoli e obiettivi specifici. Di seguito sono descritti i principali attori del sistema:

**<u>1. Utente:</u>**

È l'utente che usufruisce dei mezzi di mobilità condivisa. Deve essere registrato per utilizzare la mappa, per localizzare i mezzi, per noleggiare e pagare. Le tipologie di Utente sono:

- **Pendolare Urbano:** Persona che utilizza regolarmente il servizio per coprire l'ultimo miglio (es. da stazione a ufficio) e cerca affidabilità e abbonamenti convenienti.

- **Utente Occasionale:** Residente che utilizza il servizio saltuariamente per necessità impreviste o svago.

- **Turista:** Visitatore che necessita di un accesso rapido e senza frizioni per esplorare la città in modo sostenibile.

**<u>2. Operatore del Servizio:</u>**

Rappresenta l'azienda che immette i mezzi sulla strada. Gestisce il business e la manutenzione. Le tipologie di figure interne all'Operatore sono:

- Manager del Servizio: Definisce i piani tariffari, le promozioni, le zone operative e le zone soggette a restrizioni per massimizzare il profitto e regolare la circolazione dei mezzi.

- Team Logistico e Manutentori: Personale sul campo che si occupa della ricarica delle batterie, della riparazione dei guasti e dello spostamento fisico dei mezzi nelle zone ad alta richiesta.

**<u>3. Amministrazione Pubblica:</u>**

Ente che detiene la sovranità sul suolo pubblico e definisce le regole del gioco. Le figure coinvolte sono:

- Pianificatore Urbano/Mobility Manager: Utilizza i dati e i report aggregati della piattaforma per analizzare i flussi di mobilità, studiare nuovi percorsi ciclabili e supportare le decisioni strategiche di pianificazione urbana.

## Item funzionali

Contiene l’elenco e la specifica di tutti i requisiti funzionali espressi attraverso lo schema delle user stories:

### IF-UT.01 – Visualizza Mappa Utente

*Come* utente,

*Voglio* visualizzare la Mappa Utente,

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

### *Come* utente, 

### *Voglio* lasciare una recensione,

### *Così da* aiutare a migliorare il servizio.

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

*Voglio* visualizza la mappa,

*Così* *da* monitorare il servizio sulla citta.

### IF-OP.01 – Visualizza Mappa Operatore

*Come* operatore,

*Voglio* visualizzare la Mappa Operatore,

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

*Come* Operatore

*Voglio* Definire regole sanzionatorie per i rilasci dei mezzi al di fuori delle aree di parcheggio consentite

**Così da** garantire il decoro urbano

### IF-OP.07 - Definisce Zone 

*Come* operatore,

*Voglio* definire i confini di una Zona,

*Così* *da* garantire il rispetto delle normative locali.

### IF-OP.08 – Gestisce Segnalazioni

*Come* operatore,

*Voglio* leggere le segnalazioni inviate dagli utenti,

*Così* *da* pianificare gli interventi di manutenzione.

**Nota di implementazione (Sprint 3):** il flusso di gestione segue le transizioni di stato `aperta → in_carico → risolta`. L'operatore prende in carico una segnalazione (`PATCH /operatore/segnalazioni/{id}/prendi-in-carico`) e solo da `in_carico` può segnarla come risolta (`PATCH /operatore/segnalazioni/{id}/risolvi`); un tentativo di risolvere una segnalazione ancora `aperta` viene rifiutato con HTTP 422. Lo stato `risolta` è visibile anche lato utente nello storico delle proprie segnalazioni (`VistaSegnalazione.tsx`), senza notifica push dedicata — l'utente lo vede ricaricando/rivisitando la pagina.

### IF-OP.09– Sospende Account Utente

*Come* operatore,

*Voglio* sospendere l'account di un utente,

*Così* *da* tutelare l'integrità del servizio

### IF-OP.10– Definisce Offerte

*Come* operatore,

*Voglio* definire promozioni con condizioni e scadenza configurabili,

*Così* *da* incentivare l'utilizzo del sistema con politiche commerciali flessibili.

### IF-OP.11 – Configura Parametri Sistema 

*Come* operatore,

*Voglio* configurare i parametri relativa al sistema,

*Così* da stabilire dei limiti di utilizzo.

### IF-OP.13 – Mostra Storico Modifiche

*Come* operatore,

*Voglio* consultare un registro cronologico delle modifiche apportate al sistema,

*Così da* poter ricostruire l'evoluzione delle configurazioni del servizio.

**Nota di implementazione (Sprint 3):** la registrazione nello storico modifiche è stata estesa oltre a `parametri_sistema`, `regole_fine_corsa`, `zona_creata` e `zona_eliminata` per includere anche `tariffa_creata`, `tariffa_modificata`, `offerta_creata`, `offerta_modificata` e `offerta_eliminata` — loggate da `ServizioTariffa` e `ServizioOfferta` con la stessa convenzione testuale `"campo1=valore1, campo2=valore2"` per `valore_precedente`/`valore_nuovo`. L'interfaccia `VistaStoricoModifiche.tsx` è stata riorganizzata da un elenco cronologico piatto a un accordion con una sezione collassabile per categoria (Parametri di sistema, Regole di fine corsa, Zone, Tariffe, Offerte); ogni voce calcola un diff campo-per-campo e mostra solo i campi effettivamente cambiati, con etichette in italiano, unità di misura (€, %, minuti) e freccia "prima → dopo".

### IF-OP.12 – Visualizza Recensioni 

*Come* operatore,

*Voglio* visualizzare le recensioni lasciate dagli utenti,

cosi da avere un riscontro sulle migliorie da apportare al sistema

## Item non funzionali

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali.

### Item Informativi

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali di tipo informativo.

#### IIN-1 Prestazioni 

- Il sistema deve aggiornare la posizione dei mezzi sulla Mappa Utente entro x secondi dall'ultimo rilevamento GPS (da testare)

- Il sistema deve completare l'operazione di prenotazione di un mezzo entro x secondi dalla richiesta dell'utente (da testare)

- Il sistema deve mantenere la coerenza dei dati temporali in modo proattivo: le prenotazioni scadute (IF-UT.02) e gli abbonamenti scaduti (IF-UT.13) vengono aggiornati automaticamente tramite job schedulati nel database (pg_cron), senza dipendere dall'interazione dell'utente. I mezzi con prenotazioni scadute vengono riportati a stato `Disponibile`. Gli utenti interessati ricevono una notifica persistita nella tabella `notifiche` (entità `Notifica` già presente nel Diagramma Classi). Migrazione di riferimento: `016_cleanup_scadenze.sql`.

#### IIN-2 Sicurezza

- Tutte le comunicazioni tra client e server devono essere cifrate mediante protocolli di sicurezza standard

- Il sistema deve bloccare un account dopo 5 tentativi di autenticazione falliti consecutivi in un tempo configurabile dall’operatore

- I dati personali degli utenti devono essere trattati in conformità al Regolamento UE 2016/679 (GDPR)

- Ciascun ruolo (UT, OP, AP) deve poter accedere esclusivamente alle funzionalità ad esso assegnate

#### IIN-3 Usabilità 

- L'interfaccia deve essere accessibile secondo le linee guida WCAG (es. per utenti con disabilità visive)

- L’interfaccia deve essere facile da usare e comprensibile in meno di x minuti

#### IIN-4 Scalabilità 

- L'architettura deve permettere l'aggiunta di nuove tipologie di mezzo senza modifiche strutturali

#### IIN-5 Portabilità 

- Il sistema deve essere accessibile tramite browser web su dispositivi desktop e mobile, senza necessità di installazione

#### Conformità

- I report esportabili in CSV/PDF (AP.06) devono rispettare eventuali standard di formato richiesti dalla pubblica amministrazione

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

### Item Qualitativi

Contiene l’elenco e la specifica di tutti gli eventuali requisiti non funzionali di tipo qualitativo.

#### IQ-1

#### IQ-2

#### IQ-n

### Altri Item\

Sprint Report N. 3

**Ciclo 4**

**Smart Mobility**

# Sprint Report

## Sprint Backlog

Tabella di riepilogo che indica, per ognuno degli Sprint successivi allo Sprint n.0, la lista degli item del Product Backlog, evidenziando quelli che verranno implementati nell’ambito dello sprint corrente unitamente ad una descrizione esplicativa.

Per semplificare l’esposizione e salvaguardare la tracciabilità tra semilavorati si è proceduto alle seguenti assunzioni:

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
| UT.11 | Sprint 2 | Visualizza Storico Corsa |
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
| OP.13 | Sprint 3 | Mostra storico modifiche |
| OP.12 | Sprint 3 | Visualizza Recensioni |

## Product Requirement Specification 

### Diagramma dei Casi d’uso

<img src="media/image20.png" style="width:5.21296in;height:8.16667in" />

### Specifiche dei Casi d’uso

#### UT – 01 Visualizza Mappa utente

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
<td>Il sistema mostra all'Utente autenticato la mappa interattiva con i mezzi disponibili nelle vicinanze, le zone con restrizioni e le zone di parcheggio, così da poter scegliere un mezzo da prenotare o sbloccare.</td>
</tr>
<tr>
<td><strong>Attori Primari</strong></td>
<td>Utente</td>
</tr>
<tr>
<td><strong>Attori Secondari</strong></td>
<td>ServizioMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L’utente è autenticato alla piattaforma</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'Utente accede alla schermata principale della piattaforma.</p></li>
<li><p>Il sistema rileva la posizione geografica corrente dell'Utente tramite il dispositivo.</p></li>
<li><p>Il sistema interroga il ServizioMappa per recuperare i dati geografici.</p></li>
<li><p>Il sistema recupera le zone con restrizioni e le zone di parcheggio.</p></li>
<li><p>Il sistema visualizza la mappa con i soli mezzi disponibili per tipologia, le aree con restrizioni, le zone di parcheggio e il marker della posizione corrente.</p></li>
</ol></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>La mappa è visualizzata con i dati aggiornati; l'Utente può procedere con la prenotazione o lo sblocco di un mezzo.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>PosizioneNonDisponibile, ServizioMappa non raggiungibile</td>
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
<th><strong>Visualizza MappaUtente:</strong> PosizioneNonDisponibile</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-01.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il dispositivo non supporta la geolocalizzazione o l'Utente nega il permesso; il sistema mostra comunque la mappa centrata su una posizione di default.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>il dispositivo non supporta la geolocalizzazione o l'Utente nega il permesso.</td>
</tr>
<tr>
<td>Post-Condizioni</td>
<td style="text-align: left;">La mappa è visualizzata con i dati aggiornati ma senza il marker di posizione; l'Utente può navigare manualmente la mappa.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>2a. Il sistema rileva che la geolocalizzazione non è disponibile. </p>
<p>2b. Il sistema centra la mappa sulla posizione di default (centro di Zootropolis). </p>
<p>2c. Il sistema prosegue dal passo 3 senza visualizzare il marker della posizione corrente.</p></td>
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
<th><strong>Visualizza MappaUtente:</strong> ServizioMappa non raggiungibile</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-01.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema non riesce a interrogare il ServizioMappa a causa di un timeout o errore di rete; la mappa non viene visualizzata e l'Utente può riprovare.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Al passo 3: il sistema non riesce a interrogare il ServizioMappa (timeout o errore di rete).</td>
</tr>
<tr>
<td>Post-Condizioni</td>
<td style="text-align: left;">La mappa non viene visualizzata; il caso d'uso termina senza procedere con prenotazione o sblocco.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>3a. Il sistema rileva l'errore di comunicazione con il ServizioMappa.</p>
<p>3b. Il sistema mostra un messaggio di errore ("Impossibile caricare i dati della mappa"). </p>
<p>3c. Il sistema offre all'Utente la possibilità di riprovare. </p>
<p>3d. Se l'Utente riprova, il caso d'uso riparte dal passo 3; altrimenti termina.</p></td>
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
<p>Per ogni mezzo prenotato, il sistema aggiorna lo stato da "Disponibile" a "Prenotato" e avvia il timer di prenotazione.</p>
<p>Il sistema notifica l'Utente con la conferma di tutte le prenotazioni e il tempo rimanente.</p></td>
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
<td><p>Il caso d’uso inizia dopo il passo 7 della sequenza principale.</p>
<p>Il sistema rimuove dalla selezione i mezzi non più disponibili e informa l'Utente.</p>
<p>Il sistema mostra la lista aggiornata dei mezzi disponibili nelle vicinanze.</p>
<p>L'Utente sceglie se aggiungere un mezzo sostitutivo (torna al passo 2 del flusso principale) oppure procedere con i mezzi rimanenti.</p>
<p>Se rimane almeno un mezzo nella selezione, il sistema riprende dal passo 8 del flusso principale.</p>
<p>Se la selezione è vuota, il caso d'uso termina senza prenotazioni attive.</p></td>
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
<p>2.Il sistema mostra all'Utente i mezzi sbloccabili: quelli con prenotazione attiva a suo nome e quelli disponibili nelle vicinanze.</p>
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
<td><p>Il caso d’uso inizia dopo il passo 5 della sequenza principale</p>
<p>Il sistema rileva il timeout per uno o più mezzi e li rimuove dall'operazione di sblocco.</p>
<p>Il sistema notifica l'Utente indicando quali mezzi non è stato possibile sbloccare.</p>
<p>L'Utente può riprovare lo sblocco sui mezzi falliti o procedere con quelli già sbloccati.</p></td>
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
<td>ID</td>
<td>UT-04</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'utente autenticato di terminare la corsa in corso, verificando la posizione del mezzo e applicando le regole di fine corsa configurate dall'operatore, così da liberare il mezzo e addebitare il costo della sessione.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'utente è autenticato alla piattaforma e ha una corsa attiva.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l'utente vuole terminare e pagare la corsa.</p>
<p>2. Il sistema rileva la posizione corrente del mezzo tramite ServizioMappa.</p>
<p><em>Punto di estensione: Errore</em>ServizioMappa</p>
<p>3. Il sistema aggiorna lo stato del mezzo da "In Uso" a "Disponibile".</p>
<p>4. Il sistema mostra all'utente il Riepilogo Corsa con le varie informazioni.</p>
<p>5. <em>punto di inclusione (Visualizza Riepilogo Fine Corsa)</em></p>
<p>6.<em>include (EffettuaPagamento).</em></p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>La corsa è terminata, il mezzo è liberato e reso disponibile, l'addebito è stato effettuato e il riepilogo è mostrato all'utente.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<td>ID</td>
<td>UT-04.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema informa l'utente che il mezzo si trova in una Zona Vietata e applica una penale obbligatoria prima di consentire la fine corsa.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Il mezzo si trova in una Zona Vietata al momento della richiesta di fine corsa.</td>
</tr>
<tr>
<td>Post-Condizioni</td>
<td style="text-align: left;">La corsa è terminata con applicazione della penale obbligatoria; il mezzo è liberato e l'addebito comprensivo di penale è stato effettuato.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.</p>
<p>2. Il sistema rileva che il mezzo si trova in una Zona Vietata.</p>
<p>3. Il sistema notifica l'utente che il mezzo si trova in una Zona Vietata e che verrà applicata una penale obbligatoria.</p>
<p>4. Il sistema prosegue dal passo 3 della sequenza principale applicando la penale al costo totale della corsa.</p></td>
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
<td>ID</td>
<td>UT-05</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema addebita un importo definito sul metodo di pagamento predefinito dell'Utente, a seguito di un'operazione che prevede un costo (es. sottoscrizione di abbonamento, termine di una corsa). L'operazione avviene senza richiedere alcuna azione manuale all'utente.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Sistema</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>È stata completata un'operazione soggetta a pagamento</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando il sistema deve procedere all'addebito per un'operazione completata.</p>
<p>2. Il sistema determina l'importo dovuto sulla base delle condizioni economiche applicabili all'operazione (tariffe, piano di abbonamento, ecc.).</p>
<p>3. Il sistema recupera il metodo di pagamento predefinito dell'Utente.</p>
<p>4. Il sistema trasmette la richiesta di addebito al ProviderPagamenti.</p>
<p>5. Il ProviderPagamenti autorizza e completa la transazione.</p>
<p>6. Il sistema genera e invia la ricevuta di pagamento all'Utente.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>L'importo è stato addebitato; l'Utente riceve la ricevuta di pagamento.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td>PagamentoRifiutato</td>
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
<td>ID</td>
<td>UT-05.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il ProviderPagamenti rifiuta la transazione.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Sistema</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Il ProviderPagamenti ha restituito un esito negativo per la transazione.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>Il pagamento non è andato a buon fine; l'Utente è notificato del problema.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. La sequenza alternativa inizia dopo il passo 4 della sequenza principale.</p>
<p>2. Il sistema riceve l'esito negativo dal Sistema di Pagamento Esterno.</p>
<p>3. Il sistema notifica l'Utente del fallimento e lo invita ad aggiornare il metodo di pagamento.</p></td>
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
<td>ID</td>
<td>UT-06</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'utente autenticato di salvare uno o più metodi di pagamento sul proprio account, così da ricevere l'addebito automatico al termine di ogni corsa senza reinserire i dati.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ProviderPagamenti</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l'utente accede alla sezione "Portafoglio" dal menu laterale.</p>
<p>2. Il sistema mostra i metodi di pagamento attualmente associati all'account utente e l'opzione per aggiungerne uno nuovo.</p>
<p>3. L'utente seleziona l'opzione per aggiungere un nuovo metodo di pagamento.</p>
<p>4. Il sistema mostra le tipologie di metodo di pagamento disponibili (Google Pay, Apple Pay, PayPal, carta di credito).</p>
<p>5. L'utente seleziona la tipologia desiderata e inserisce i dati richiesti.</p>
<p>6. Il sistema valida i dati inseriti tramite ProviderPagamenti. Se ProviderPagamenti restituisce un errore di validazione, il sistema informa l'utente che i dati inseriti non sono validi e torna al passo 5.</p>
<p>7. Il sistema verifica che il metodo di pagamento non sia già associato all'account. Se è già presente, il sistema informa l'utente e non procede al salvataggio.<br />
8. Il sistema salva il nuovo metodo di pagamento sull'account utente.</p>
<p>9. Se il metodo appena salvato è il primo associato all'account, il sistema lo imposta automaticamente come predefinito. Altrimenti, il sistema chiede all'utente se desidera impostarlo come nuovo metodo predefinito.</p>
<p>10. Se l'utente conferma, il sistema aggiorna il metodo predefinito con quello appena salvato.<br />
11. Il sistema mostra un messaggio di conferma all'utente.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>Il nuovo metodo di pagamento è stato salvato sull'account utente. Il metodo predefinito è quello scelto dall'utente, o il primo salvato se non è stata effettuata alcuna scelta esplicita.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td style="text-align: left;">Nessuna</td>
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
<th>Nome</th>
<th>Consulta Tariffe</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT.07</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema mostra all'Utente autenticato il tariffario attivo per ciascuna tipologia di mezzo disponibile (Monopattino, Bicicletta, Automobile), indicando il costo al minuto e il costo al chilometro, così da consentirgli di confrontare i costi prima di effettuare una prenotazione.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'Utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione "Piano Tariffario" dal menu laterale.</p>
<p>2. Il sistema recupera le tariffe attualmente definite dall'Operatore per ciascuna tipologia di mezzo.</p>
<p>3. Il sistema presenta il tariffario con una card per tipologia di mezzo (Monopattino, Bicicletta, Automobile), indicando per ciascuna il costo al minuto e il costo al chilometro.</p>
<p>4. L'Utente consulta le tariffe visualizzate.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>L'Utente ha visualizzato il tariffario aggiornato e può procedere con la scelta del mezzo più adatto alle proprie esigenze.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>ConsultaTariffe: TariffeNonDefinite</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-07.01</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>L'Operatore non ha ancora definito le tariffe per una o più tipologie di mezzo.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Non sono presenti tariffe definite dall'Operatore per almeno una tipologia di mezzo.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>Il tariffario non viene mostrato completamente; l'Utente è informato che le tariffe non sono ancora disponibili.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Visualizza Riepilogo Fine Corsa</th>
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
<td><p>Il sistema presenta all'Utente il riepilogo per ogni mezzo.</p>
<p>Se la corsa coinvolgeva più di un mezzo:</p>
<p>2.1 il sistema mostra il costo totale complessivo della sessione di gruppo.</p>
<p>L'Utente prende visione del riepilogo e lo chiude.</p></td>
</tr>
<tr>
<td><strong>Post-condizioni</strong></td>
<td>Il riepilogo è stato visualizzato; il riepilogo di ogni mezzo è disponibile nello storico corse del profilo.</td>
</tr>
<tr>
<td><strong>Sequenza alternativa degli eventi</strong></td>
<td>RiepilogoDaFallBack</td>
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
<th>Nome</th>
<th>VisualizzaRiepilogoFineCorsa: RiepilogoDaFallBack</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-08.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema non riesce a recuperare dal backend il riepilogo della corsa appena conclusa (es. corsa non trovata o errore di comunicazione). Per garantire che il riepilogo sia sempre disponibile, il sistema lo ricostruisce dai dati già presenti sul client (corse terminate e pagamenti effettuati) e lo presenta comunque all'Utente.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>La procedura Termina Corsa si è conclusa con successo, ma il recupero del riepilogo dal backend non va a buon fine.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>Il riepilogo viene comunque visualizzato all'Utente, costruito dai dati locali (costo totale, durata, mezzi della sessione); l'esperienza dell'Utente non cambia.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. La sequenza alternativa si attiva al passo 1 della sequenza principale, quando il recupero del riepilogo dal backend fallisce.</p>
<p>2. Il sistema rileva l'esito negativo della richiesta</p>
<p>3. Il sistema ricostruisce il riepilogo a partire dai dati della sessione già disponibili sul client.</p>
<p>4. Il sistema presenta all'Utente il riepilogo ricostruito.</p>
<p>5. Il flusso prosegue dal passo 3 della sequenza principale.</p></td>
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
<th>Nome</th>
<th>Sospende corsa</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-09</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'utente autenticato con una corsa attiva di mettere temporaneamente in pausa la corsa, bloccando il mezzo senza terminare la sessione, così da effettuare soste mantenendo il possesso del mezzo. La pausa è gratuita entro il periodo di grazia configurato dall'operatore; al suo termine viene applicata la politica di addebito configurata.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L’utente è autenticato e ha una corsa attiva</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'utente vuole mettere in pausa la corsa in corso.</p>
<p>2. Il sistema invia il comando di blocco temporaneo al mezzo.</p>
<p>3. Il mezzo conferma l'avvenuto blocco al sistema.</p>
<p>4. Il sistema aggiorna lo stato del mezzo da "In Uso" a "In Pausa" e registra l'istante di inizio pausa.</p>
<p>5. Il sistema avvia il conteggio del periodo di grazia configurato dall'operatore.</p>
<p>6. Il sistema notifica all'utente che la corsa è stata sospesa, indicando il tempo di pausa gratuita residuo e l'eventuale politica di addebito successiva.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>La corsa non è terminata; il mezzo è bloccato e resta riservato all'utente nello stato "In Pausa"; il sistema mantiene attiva la sessione e traccia la durata della pausa</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>SospendeCorsa: Superamento Periodo di Grazia</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-09.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>La pausa si protrae oltre il periodo di grazia e il sistema applica la politica di addebito per pausa configurata dall'operatore.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>La durata della pausa ha raggiunto il periodo di grazia configurato dall'operatore.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>La corsa resta sospesa con applicazione dell'addebito per pausa secondo la politica configurata; la sessione rimane attiva</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Visualizza Promozioni</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT.10</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema mostra all'Utente autenticato l'elenco delle promozioni attive pubblicate dall'Operatore, con le relative condizioni e vantaggi, così da consentirgli di ridurre i costi di utilizzo del servizio.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'Utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione "Bonus e Promozioni" dal menu laterale.</p>
<p>2. Il sistema recupera l'elenco delle promozioni attive pubblicate dall'Operatore.</p>
<p>3. Il sistema presenta l'elenco delle promozioni disponibili, indicando per ciascuna: tipologia, descrizione, condizioni di applicazione e data di scadenza.</p>
<p>4. L'Utente consulta le promozioni disponibili.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>L'Utente ha visualizzato l'elenco delle promozioni attive e può scegliere di usufruirne nelle corse successive.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>VisualizzaPromozioni: NessunPromozioneAttiva</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-10.01</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Non vi sono promozioni attive pubblicate dall'Operatore al momento della richiesta.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Non vi sono promozioni attive pubblicate dall'Operatore.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>L'elenco delle promozioni non viene mostrato; l'Utente è informato dell'assenza di promozioni attive.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Visualizza Storico Corse</th>
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
<th>Nome</th>
<th>Visualizza Storico Corse: DatiNonDisponibili</th>
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
<th>Nome</th>
<th>Invia segnalazione</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-12</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Utente autenticato di inviare una segnalazione relativa a un mezzo o a una situazione anomala, così da informare l'Operatore affinché possa intervenire tempestivamente.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'utente è autenticato alla piattaforma.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione dedicata alle segnalazioni.</p>
<p>2. Il sistema mostra il form di segnalazione con i campi richiesti.</p>
<p>3. L'Utente seleziona la tipologia di segnalazione.</p>
<p>4. L'Utente compila i campi richiesti e conferma l'invio.</p>
<p>5. Il sistema registra la segnalazione e la rende visibile all'Operatore.</p>
<p>6. Il sistema notifica l'Utente dell'avvenuto invio della segnalazione.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>La segnalazione è registrata nel sistema e resa disponibile all'Operatore per la presa in carico.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Sottoscrive Abbonamento</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-13</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Utente autenticato di scegliere e sottoscrivere un piano di abbonamento attivo, così da usufruire di condizioni tariffarie agevolate per un periodo determinato.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td><p>1. L'utente è autenticato alla piattaforma;</p>
<p>2. esistono piani di abbonamento attivi pubblicati dall'operatore</p>
<p>3. l'utente ha un metodo di pagamento valido.</p></td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Utente accede alla sezione dedicata agli abbonamenti.</p>
<p>2. Il sistema recupera e mostra i piani di abbonamento disponibili, con durata, costo e benefici di ciascuno.</p>
<p>3. L'utente seleziona il piano desiderato.</p>
<p>4. Il sistema mostra il riepilogo del piano selezionato e richiede conferma.</p>
<p>5. L'utente conferma la sottoscrizione.</p>
<p>6. Include (EffettuaPagamento).</p>
<p>7. Il sistema attiva l'abbonamento sull'account dell'utente a partire dalla data corrente.</p>
<p>8. Il sistema notifica l'utente dell'avvenuta attivazione.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>L'abbonamento è attivo sull'account dell'utente; le condizioni tariffarie agevolate sono applicate a partire dalla data di attivazione.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td>Nessuno</td>
</tr>
</tbody>
</table>

#### UT – 14 Visualizza Suggerimenti Intelligenti

<table style="width:100%;">
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
<th>Nome</th>
<th>Visualizza Suggerimenti Intelligenti: DatiInsufficienti</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>UT-14.01</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il ServizioAI valuta che i dati storici dell'Utente non sono ancora sufficienti per produrre suggerimenti significativi e restituisce una lista vuota con segnale esplicito.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Utente</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>ServizioAI</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Il ServizioAI ha ricevuto i dati dell'Utente e ha determinato autonomamente che non sono sufficienti per generare suggerimenti utili.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>Nessun suggerimento viene mostrato; l'Utente è informato della necessità di continuare a utilizzare il servizio.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. La sequenza alternativa sostituisce i passi 5–6 della sequenza principale.</p>
<p>2. Il ServizioAI restituisce al sistema una lista vuota con un messaggio che indica l’insufficienza dei dati.</p>
<p>3. Il sistema notifica l'Utente che non è ancora possibile generare suggerimenti personalizzati e lo invita a continuare a utilizzare il servizio.</p></td>
</tr>
</tbody>
</table>

#### UT – 15 Scrive Recensione

<table style="width:100%;">
<colgroup>
<col style="width: 24%" />
<col style="width: 75%" />
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
<td>Nessuno</td>
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
<th>Nome</th>
<th>Accede Report</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>AP-01</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Amministrazione Pubblica autenticata di consultare la dashboard di reportistica aggregata sull'utilizzo del servizio di mobilità condivisa, visualizzando statistiche su corse effettuate, chilometri percorsi e distribuzione per tipologia di mezzo, così da supportare decisioni strategiche di pianificazione urbana.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'Amministrazione Pubblica è autenticata alla piattaforma con il ruolo AP.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Amministrazione Pubblica seleziona l'opzione "Visualizza Report" dalla propria dashboard.</p>
<p>2. Il sistema recupera le statistiche aggregate sull'utilizzo del servizio relative all'intervallo temporale configurato.</p>
<p>3. Il sistema presenta la dashboard di reportistica con un istogramma a barre impilate che analizza il volume dei noleggi su base settimanale e un grafico a torta che illustra la quota di mercato per tipologia di mezzo.</p>
<p>4. L'Amministrazione Pubblica consulta i dati visualizzati.</p>
<p>5. Punto di estensione: EsportaReport (si attiva se l'Amministrazione Pubblica seleziona una delle opzioni di esportazione disponibili).</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>La dashboard di reportistica è visualizzata con i dati aggregati aggiornati; l'Amministrazione Pubblica ha consultato le statistiche sull'utilizzo del servizio.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>AccedeReport: DatiNonDisponibili</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>AP-01.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema non riesce a recuperare le statistiche aggregate a causa di un errore nel sistema di elaborazione dati.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Il sistema non è in grado di accedere o elaborare i dati aggregati del report.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>La dashboard di reportistica non viene mostrata; l'Amministrazione Pubblica è informata del problema temporaneo.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Esporta Report</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>AP-02</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Amministrazione Pubblica di esportare il report aggregato correntemente visualizzato in uno dei formati disponibili (CSV o PDF), così da poterlo utilizzare in analisi esterne e documentazione ufficiale. Questo caso d'uso estende AccedeReport.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td><p>L'Amministrazione Pubblica ha acceduto alla dashboard di reportistica (CS-14).</p>
<p>I dati del report sono disponibili e visualizzati correttamente.</p></td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia dal Punto di estensione EsportaReport di AccedeReport, quando l'Amministrazione 2. Pubblica seleziona una delle opzioni di esportazione disponibili.</p>
<p>3. Il sistema presenta le opzioni di formato disponibili: CSV e PDF.</p>
<p>4. L'Amministrazione Pubblica seleziona il formato desiderato.</p>
<p>5. Il sistema genera il file nel formato selezionato contenente i dati del report aggregato correntemente visualizzato.</p>
<p>6. Il sistema avvia il download del file sul dispositivo dell'Amministrazione Pubblica.</p>
<p>7. Il sistema notifica l'Amministrazione Pubblica del completamento dell'esportazione.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>Il file del report aggregato è stato generato e scaricato nel formato selezionato; i dati esportati corrispondono alle statistiche visualizzate nella dashboard.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>EsportaReport: ErroreGenerazioneFile</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>AP-02.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema non riesce a generare il file di esportazione nel formato selezionato.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Il sistema ha incontrato un errore durante la generazione del file nel formato selezionato.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>Il file non viene generato; l'Amministrazione Pubblica è informata del problema e può ritentare l'operazione.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Visualizza Mappa Amministrazione Pubblica</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>AP-03</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema mostra all'Amministrazione Pubblica autenticata la mappa interattiva dell'area urbana di competenza, arricchita da layer statistici sovrapposti — tra cui la heatmap della distribuzione dei mezzi, l'intensità d'uso per zona e le aree a bassa disponibilità — così da supportare decisioni strategiche di pianificazione e monitoraggio del servizio sul territorio.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'Amministrazione Pubblica è autenticata alla piattaforma con il ruolo AP.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Amministrazione Pubblica accede alla schermata principale della propria dashboard.</p>
<p>2. Il sistema interroga il ServizioMappa per recuperare i dati geografici aggiornati relativi all'area urbana di competenza.</p>
<p>3. Il sistema carica la mappa interattiva e sovrappone il layer predefinito: la heatmap della distribuzione dei mezzi, che evidenzia con gradiente cromatico le aree ad alta e bassa densità di mezzi disponibili.</p>
<p>4. Il sistema visualizza sulla mappa le zone definite (Operativa, Vietata, Limitata, di Parcheggio) con la rispettiva colorazione semantica.</p>
<p>5. Il sistema mostra nel pannello laterale i layer statistici selezionabili: distribuzione mezzi per tipologia, intensità d'uso per zona e fasce orarie di picco.</p>
<p>6. L'Amministrazione Pubblica seleziona i layer statistici di interesse da visualizzare sulla mappa.</p>
<p>7. Il sistema aggiorna la mappa mostrando i layer selezionati.</p>
<p>8. L'Amministrazione Pubblica consulta i dati territoriali visualizzati.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>La mappa è visualizzata con i layer statistici selezionati e aggiornati; l'Amministrazione Pubblica può monitorare la distribuzione dei mezzi sul territorio e procedere con decisioni strategiche di pianificazione urbana.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td>DatiGISNonDisponibili</td>
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
<th>Nome</th>
<th>VisualizzaMappaAP: DatiGISNonDisponibili</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>AP-03.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il ServizioMappa non riesce a fornire i dati geografici o statistici necessari al caricamento della mappa.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Amministrazione Pubblica</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Il ServizioMappa ha restituito un errore o non è raggiungibile al momento della richiesta.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>La mappa non viene caricata; l'Amministrazione Pubblica è informata dell'indisponibilità temporanea del servizio cartografico.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. La sequenza alternativa inizia dopo il passo 2 della sequenza principale.</p>
<p>2. Il sistema rileva che il ServizioMappa non ha restituito dati validi.</p>
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
<td>ServizioMappa</td>
</tr>
<tr>
<td><strong>Precondizioni</strong></td>
<td>L’operatore è autenticato alla piattaforma</td>
</tr>
<tr>
<td><strong>Sequenza principale degli eventi</strong></td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'Operatore accede alla schermata principale della piattaforma.</p></li>
<li><p>Il sistema interroga il ServizioMappa per recuperare i dati geografici.</p></li>
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
<td>ID</td>
<td>OP – 02</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'operatore autenticato di aggiungere un nuovo mezzo alla flotta, specificando tipologia, identificativo, posizione iniziale e stato, così da renderlo disponibile per il noleggio da parte degli utenti.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore è autenticato alla piattaforma e si trova nella Dashboard Operatore.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td>1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata ai mezzi.</td>
</tr>
<tr>
<td><p>2. Il sistema mostra la lista dei mezzi attualmente presenti nella flotta.</p>
<p>3. L'operatore seleziona la funzione che permette di aggiungere un nuovo mezzo.</p>
<p>4. Il sistema permette di inserire i campi: tipologia (monopattino, bicicletta, automobile), identificativo, posizione iniziale e stato iniziale.</p>
<p>5. L'operatore inserisce i dati richiesti e seleziona la posizione iniziale sulla mappa.</p>
<p>6. L'operatore conferma i dati inseriti.</p>
<p>7. Il sistema valida i dati verificando che i campi obbligatori siano compilati e che l'identificativo sia univoco. Se uno o più campi non sono validi, il sistema informa l'operatore specificando i campi non validi e torna al passo 5.</p>
<p>8. Il sistema verifica tramite ServizioMappa che la posizione selezionata ricada all'interno di una zona operativa.</p>
<p>9. Il sistema salva il nuovo mezzo associandolo alla flotta.</p>
<p>10. Il sistema mostra un messaggio di conferma all'operatore.</p>
<p>Post-condizioni</p></td>
<td>Il nuovo mezzo è stato salvato nel sistema e risulta disponibile sulla Mappa Utente in base allo stato impostato.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td>IdentificativoEsistentePosizioneNonOperativa</td>
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
<td>ID</td>
<td>OP – 03</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'operatore autenticato di dismettere un mezzo precedentemente censito, rimuovendone la disponibilità per l'assegnazione a nuove missioni e mantenendone lo storico ai fini di consultazione.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore deve essere autenticato nel sistema e il mezzo da dismettere deve essere già censito e non assegnato ad alcuna missione attiva.</td>
</tr>
<tr>
<td>Sequenza principale</td>
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
<td>Post-condizioni</td>
<td>Il mezzo è registrato come dismesso nel sistema, non risulta più disponibile per l'assegnazione a nuove corse e i dati storici relativi al mezzo rimangono consultabili.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<td>ID</td>
<td>OP-03.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema informa l'operatore che il mezzo selezionato è attualmente impegnato in una missione e non può essere dismesso.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>ServizioMappa</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore deve essere autenticato nel sistema e il mezzo selezionato risulta assegnato a una corsa attiva.</td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>Lo stato del mezzo resta invariato e l'operatore rimane nella sezione di gestione dei mezzi.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. Il sistema, tramite il ServizioMappa, rileva che il mezzo selezionato è impegnato in una corsa.</p>
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
<td>ID</td>
<td>OP-04</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'operatore autenticato di modificare lo stato di un mezzo della flotta, così da nasconderlo o mostrarlo sulla Mappa Utente e gestire il ciclo operativo del veicolo.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore è autenticato alla piattaforma e il mezzo selezionato esiste nella flotta.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
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
<td>Post-condizioni</td>
<td>Lo stato del mezzo è stato aggiornato. Se il nuovo stato è "In manutenzione" o "Fuori servizio" il mezzo non è più visibile sulla Mappa Utente; se il nuovo stato è "Disponibile" il mezzo è nuovamente visibile sulla Mappa Utente</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th><strong>Modifica Stato Mezzo: MezzoInUso</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>OP-04.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema informa l'operatore che il mezzo selezionato è attualmente in uso da un utente e non può essere modificato.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Il mezzo selezionato ha stato "In uso" o "Prenotato" al momento della richiesta di modifica.</td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>Nessuna. Lo stato del mezzo non viene modificato.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. La sequenza alternativa inizia dopo il passo 6 della sequenza principale.</p>
<p>2. Il sistema rileva che il mezzo è attualmente in uso o prenotato da un utente.</p>
<p>3. Il sistema informa l'operatore che non è possibile modificare lo stato del mezzo mentre è in uso o prenotato</p></td>
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
<td>ID</td>
<td>OP-05</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'operatore autenticato di definire una nuova tariffa per una specifica tipologia di mezzo, scegliendo se applicare un costo al minuto oppure un costo al chilometro, così da permettere la configurazione del modello di costo del servizio.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore è autenticato alla piattaforma e non esiste già una tariffa definita per la tipologia di mezzo selezionata.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l'operatore accede alla sezione dedicata alle tariffe.</p>
<p>2. Il sistema mostra le tariffe attualmente definite per ciascuna tipologia di mezzo disponibile.</p>
<p>3. L'operatore seleziona la tipologia di mezzo per cui intende definire una nuova tariffa (monopattino, bicicletta, automobile).</p>
<p>4. Il sistema mostra il form di inserimento, chiedendo all'operatore di scegliere il tipo di tariffa: costo al minuto o costo al chilometro.</p>
<p>5. L'operatore seleziona il tipo di tariffa e inserisce il valore del costo richiesto.</p>
<p>6. Il sistema valida il dato inserito verificando che il valore sia numerico e maggiore di zero.</p>
<p>7. Il sistema salva la nuova tariffa, associandola alla tipologia di mezzo selezionata e al tipo di costo scelto.</p>
<p>8. Il sistema mostra un messaggio di conferma all'operatore.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>La nuova tariffa è stata salvata nel sistema, con il tipo di costo scelto dall'operatore, e sarà applicata alle corse successive effettuate con la tipologia di mezzo selezionata.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td>TariffaGiaEsistente</td>
</tr>
</tbody>
</table>

#### OP-05.1 Definisce Tariffa: TariffaGiaEsistente

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
<td>ID</td>
<td>OP-05.1</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>L'Operatore tenta di definire una tariffa per una tipologia di mezzo che ne ha già una attiva; il sistema rifiuta l'operazione.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Al passo 6 (validazione) della sequenza principale di OP-05: esiste già una tariffa definita per la tipologia di mezzo selezionata.</td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>Nessuna nuova tariffa viene salvata; la tariffa esistente resta invariata; l'Operatore è informato dell'errore.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td style="text-align: left;"><p>6a. Il sistema rileva che esiste già una tariffa per la tipologia selezionata.</p>
<p>6b. Il sistema rifiuta la richiesta.</p>
<p>6c. Il sistema informa l'Operatore che la tariffa esiste già e lo invita a usare la funzione di modifica.</p></td>
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
<td>Nome</td>
<td>Definisce Regole Fine Corsa</td>
</tr>
<tr>
<td>ID</td>
<td>OP-06</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>L'operatore definisce le regole sanzionatorie e incentivanti che governano la corretta conclusione di una corsa, specificando la politica sanzionatoria applicata al rilascio del mezzo al di fuori delle zone di parcheggio e un eventuale bonus riconosciuto all'utente al raggiungimento di un numero prestabilito di parcheggi corretti, così da garantire il decoro urbano.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore è autenticato nel sistema ed esiste almeno una zona di parcheggio già definita.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><ol type="1">
<li><p>Il caso d'uso inizia quando l'operatore accede alla sezione dedicata alle Regole Fine Corsa.</p></li>
<li><p>Il sistema mostra i parametri configurabili correnti.</p></li>
<li><p>L'operatore configura le regole:</p></li>
</ol>
<blockquote>
<p>3.1 stabilisce la politica sanzionatoria applicata al rilascio del mezzo fuori dalle zone di parcheggio (penale, blocco fine corsa o avviso);</p>
<p>3.1.2 se la politica prevede una penale, inserisce l'importo da addebitare in aggiunta al costo della corsa;</p>
<p>3.2 se intende attivare un incentivo, configura il bonus indicando il numero di parcheggi corretti necessari e il valore del bonus.</p>
</blockquote>
<ol start="4" type="1">
<li><p>L'operatore conferma le regole definite.</p></li>
<li><p>Se i parametri non rientrano negli intervalli ammessi, il sistema informa l'operatore specificando i campi non validi e torna al passo 3.</p></li>
<li><p>Il sistema salva la nuova configurazione.</p></li>
<li><p>Il sistema notifica all'operatore l'avvenuta definizione delle regole.</p></li>
</ol></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>Le nuove regole di fine corsa sono memorizzate nel sistema e vengono applicate a tutte le corse successive.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<td>ID</td>
<td>OP - 07</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>L’operatore definisce i confini geografici di una Zona caratteristica (Vietata, Limitata, di Parcheggio, Confine Operativo); il sistema memorizza la zona e la applica attivamente.</td>
</tr>
<tr>
<td>Attori primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L’operatore è autenticato con il ruolo appropriato nel sistema</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td style="text-align: left;"><p>1. Il caso d'uso inizia quando l’operatore intende definire una zona caratteristica all’interno del sistema.</p>
<p>2. Il sistema visualizza la mappa interattiva dell'area di competenza con le zone esistenti.</p>
<p>3. L’operatore disegna il perimetro della zona sulla mappa definendo i vertici del poligono.</p>
<p>4. L’operatore conferma la creazione della zona.</p>
<p>5. Fintantoché il perimetro non è valido:</p>
<p>5.1 Il sistema notifica l’operatore del problema rilevato.</p>
<p>5.2 l’operatore corregge il perimetro (torna al passo 3).</p>
<p>6. Il sistema salva la Zona e la rende attiva.</p>
<p>7. Il sistema aggiorna la mappa visibile agli Utenti evidenziando la nuova zona.</p></td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>La nuova Zona creata è persistita nel sistema con il perimetro definito; il sistema la applica alla flotta.</td>
</tr>
<tr>
<td>Sequenze alternative</td>
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
<th>Nome</th>
<th>Gestisce segnalazione</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>OP-08</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Operatore autenticato di consultare le segnalazioni inviate dagli Utenti così da pianificare gli opportuni interventi a fronte delle problematiche riscontrate (relative ai mezzi, alle zone di parcheggio o ad altri aspetti del servizio)</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore è autenticato alla piattaforma.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione dedicata alle segnalazioni.</p>
<p>2. Il sistema recupera l'elenco delle segnalazioni inviate dagli Utenti.</p>
<p>3. Il sistema presenta l'elenco delle segnalazioni in ordine cronologico, indicando per ciascuna: tipologia, descrizione e data di invio.</p>
<p>4. L'Operatore consulta le segnalazioni visualizzate.</p>
<p>5. L'Operatore seleziona una segnalazione per visualizzarne il dettaglio.</p>
<p>6. Il sistema mostra il dettaglio completo della segnalazione selezionata.</p>
<p>7. L'Operatore prende in carico la segnalazione.</p>
<p>8. Il sistema aggiorna lo stato della segnalazione e notifica l'Utente della presa in carico.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>La segnalazione è stata presa in carico dall'Operatore; l'Utente è informato dell'aggiornamento di stato.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Sospende account utente</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>OP-09</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Operatore autenticato di sospendere l'account di un Utente, così da tutelare l'integrità del servizio in caso di comportamenti scorretti o violazioni delle condizioni d'uso.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td><p>1. L'Operatore è autenticato alla piattaforma.</p>
<p>2. L'account dell'Utente da sospendere è attivo.</p></td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione per la gestione degli utenti.</p>
<p>2. Il sistema presenta l'elenco degli utenti registrati. 3. L'Operatore seleziona l'Utente di cui intende sospendere l'account.</p>
<p>4. Il sistema mostra il dettaglio del profilo dell'Utente selezionato.</p>
<p>5. L'Operatore aggiunge una descrizione sulla motivazione della sospensione dell'account e seleziona la durata della sospensione (in giorni).</p>
<p>6. L'Operatore seleziona l'opzione per sospendere Account.</p>
<p>7. Il sistema richiede conferma dell'operazione.</p>
<p>8. L'Operatore conferma la sospensione.</p>
<p>9. Il sistema sospende l'account dell'Utente per la durata indicata, calcolando la data di fine sospensione, e gli impedisce l'accesso alla piattaforma.</p>
<p>10. Il sistema notifica l'Utente dell'avvenuta sospensione del proprio account.</p>
<p>11. Allo scadere della durata, il sistema riattiva automaticamente l'account e notifica l'Utente della riattivazione.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>L'account dell'Utente è sospeso fino alla data di fine sospensione; l'Utente non può più accedere alla piattaforma finché la sospensione è attiva; l'Utente è stato notificato dell'avvenuta sospensione. Allo scadere della durata l'account torna automaticamente attivo.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<th>Nome</th>
<th>Definisce Offerta</th>
</tr>
</thead>
<tbody>
<tr>
<td>ID</td>
<td>OP-10</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Operatore autenticato di creare e pubblicare offerte commerciali (promozioni e piani di abbonamento) con condizioni e scadenza configurabili, così da incentivare l'utilizzo del servizio con politiche commerciali flessibili.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'operatore è autenticato alla piattaforma.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione delle Tariffe e Promozioni.</p>
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
<td>Post-condizioni</td>
<td>L'offerta è salvata nel sistema e resa visibile agli utenti nelle sezioni dedicate</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td>Nessuno</td>
</tr>
</tbody>
</table>

#### OP-11 Configura parametri di sistema

<table style="width:99%;">
<colgroup>
<col style="width: 28%" />
<col style="width: 70%" />
</colgroup>
<tbody>
<tr>
<td>Nome</td>
<td>Configura Parametri Numerici di Sistema</td>
</tr>
<tr>
<td>ID</td>
<td>OP-11</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>L'operatore configura i parametri numerici operativi del sistema.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L’operatore è autenticato nel sistema</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d’uso inizia quando l’operatore accede alla sezione di configurazione dei parametri di sistema.</p>
<p>2. Il sistema recupera e mostra i valori correnti dei parametri.</p>
<p>3. L’operatore inserisce i nuovi valori dei parametri che intende modificare.</p>
<p>4. L’operatore conferma le modifiche.</p>
<p>5. Se il sistema rileva che uno o più valori non rispettano i vincoli di validazione (non numerici, negativi), viene restituito un errore e il caso d’uso riprende al passo 3</p>
<p>6. Altrimenti Il sistema salva i nuovi parametri.</p>
<p>7. Il sistema mostra un messaggio di conferma all’operatore.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>I nuovi parametri numerici sono salvati nel sistema e applicati a tutte le operazioni successive.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<td>Nome</td>
<td>Visualizza Recensioni</td>
</tr>
<tr>
<td>ID</td>
<td>OP-12</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Il sistema consente all'Operatore autenticato di consultare l'elenco
delle recensioni lasciate dagli utenti (voto da 1 a 5, commento testuale
e data di creazione), insieme al voto medio aggregato, così da avere un
riscontro sulle migliorie da apportare al servizio.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>L'Operatore è autenticato alla piattaforma con il ruolo OP.</td>
</tr>
<tr>
<td>Sequenza principale degli eventi</td>
<td><p>1. Il caso d'uso inizia quando l'Operatore accede alla sezione
"Recensioni".</p>
<p>2. Il sistema recupera l'elenco delle recensioni pubblicate dagli
utenti e calcola il voto medio aggregato.</p>
<p>3. Il sistema presenta l'elenco delle recensioni, indicando per
ciascuna il voto, il commento e la data, insieme al voto medio
complessivo.</p>
<p>4. L'Operatore consulta le recensioni visualizzate.</p></td>
</tr>
<tr>
<td>Post-condizioni</td>
<td>L'elenco delle recensioni e il voto medio sono visualizzati;
l'Operatore ha consultato i feedback degli utenti.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
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
<td>Nome</td>
<td>Visualizza Recensioni: NessunaRecensione</td>
</tr>
<tr>
<td>ID</td>
<td>OP-12.01</td>
</tr>
<tr>
<td>Breve descrizione</td>
<td>Non è presente alcuna recensione pubblicata dagli utenti al momento
della richiesta.</td>
</tr>
<tr>
<td>Attori Primari</td>
<td>Operatore</td>
</tr>
<tr>
<td>Attori Secondari</td>
<td>Nessuno</td>
</tr>
<tr>
<td>Precondizioni</td>
<td>Non sono presenti recensioni nel sistema.</td>
</tr>
<tr>
<td>Postcondizioni</td>
<td>L'elenco delle recensioni non viene mostrato; l'Operatore è informato
che non sono ancora presenti recensioni.</td>
</tr>
<tr>
<td>Sequenza alternativa degli eventi</td>
<td><p>1. La sequenza alternativa sostituisce i passi 2 e 3 della sequenza
principale.</p>
<p>2. Il sistema verifica che non sia presente alcuna recensione.</p>
<p>3. Il sistema notifica all'Operatore che non sono ancora disponibili
recensioni.</p></td>
</tr>
</tbody>
</table>

## System Architecture

### Diagramma delle Componenti – Diagramma Generale

<img src="media/image21.png" style="width:6.26806in;height:4.59653in" />

#### Client

<img src="media/image22.png" style="width:4.41119in;height:8.15833in" />

#### Server

<img src="media/image23.png" style="width:6.26806in;height:4.81181in" />

### Specifica delle componenti

L’architettura portante del sistema segue il modello Client-Server, arricchito dall'integrazione del pattern logico MVC (Model-View-Controller), da un'estensione su più livelli e dalla comunicazione con servizi esterni.

#### Specifica delle componenti client

Il blocco Client gestisce l'interfaccia utente (Frontend) e la comunicazione iniziale con il server tramite le API.

**<u>VIEW</u>**: Gestisce l'interfaccia grafica e l'interazione con le diverse tipologie di utenti del sistema

- **VistaAuth:** Gestisce l'autenticazione. Contiene la classe:

  - **VistaLogin:** Schermata per l'inserimento delle credenziali (username e password) e l'accesso al sistema.

- **VistaUtente:** Interfaccia per il cliente finale. Contiene le classi:

  - VistaHomePageUtente: Schermata principale per l'utente, mostra la mappa geografica con la posizione in tempo reale dei mezzi disponibili.

  - VistaCorsa: Schermata attiva durante il noleggio, mostra i dati in tempo reale (tempo trascorso, costo stimato, pulsante per terminare la corsa).

  - VistaSegnalazioneUtente: Schermata che permette all’utente di inviare una segnalazione.

  - VistaPagamento: Schermata dedicata ai pagamenti.

  - VistaAbbonamenti: Schermata che permette di mostrare all’utente gli abbonamenti offerti dalla piattaforma.

- **VistaOperatore:** Interfaccia per il personale di gestione sul campo. Contiene le classi:

  - VistaDashBoardOperatore: È la schermata principale di controllo per l'operatore. Fornisce una panoramica dello stato del servizio, notifiche in tempo reale su eventuali anomalie dei mezzi, segnalazioni degli utenti o task di manutenzione da completare.

  - VistaDefinisciZona: Interfaccia grafica che permette all'operatore di tracciare e definire nuove aree operative sulla mappa o di modificare quelle esistenti. Viene utilizzata per impostare aree di geofencing, come zone di parcheggio obbligatorio, zone in cui è vietata la sosta o aree a velocità limitata.

  - VistaTariffePromozioni: Schermata per la gestione e la configurazione economica del servizio. Permette all'operatore di inserire nuovi piani tariffari (es. costo di sblocco e costo al minuto) o di creare e attivare codici promozionali e sconti per gli utenti.

  - VistaMezziOperatore: Pannello tecnico focalizzato sulla gestione fisica della flotta. Consente di visualizzare l'elenco completo dei veicoli, filtrandoli per stato (es. carica bassa, in manutenzione, disponibile), e include le funzionalità per registrare un nuovo mezzo nel sistema o forzare la chiusura di una corsa.

  - VistaImpostazioniRegole: Schermata di configurazione aziendale e sistemistica in cui l'operatore definisce i parametri generali di funzionamento e le regole di fine corsa (ad esempio, l'obbligo per l'utente di scattare una foto al mezzo parcheggiato prima di poter chiudere il noleggio).

  - VistaSegnalazioneOP: Schermata per la gestione e le risposte alle segnalazioni utente. L’operatore può prendere in carico la segnalazione.

  - VistaParametriSistema: Schermata di configurazione dei parametri di sistema tra cui: il numero massimo di mezzi prenotabili da un utente, i minuti del periodo di pausa e il relativo addebito e i minuti massimi per la prenotazione di un mezzo.

- VistaAmministrazionePubblica**:** Interfaccia dedicata agli enti pubblici per il monitoraggio. Contiene la classe

  - VistaDashboardAP: Interfaccia di monitoraggio riservata alla Pubblica Amministrazione per visionare dati aggregati sul traffico e sull'uso del servizio.

**<u>API SERVICE LAYER</u>**: Funge da intermediario tra le Viste (interfaccia) e il Server, esponendo o consumando i servizi di rete tramite l'interfaccia **APIToView**. **Le classi** incluse:

- ApiService: Classe di base per la gestione delle richieste HTTP (GET, POST, ecc.) e per la cattura e visualizzazione degli errori di rete.

- AuthService: Gestisce le chiamate API relative ai token di accesso, login e logout.

- PaymentService: Invia le richieste di transazione finanziaria e salvataggio dei metodi di pagamento.

- ReportService: Richiede al server i dati analitici per la generazione dei report.

- MapService: Interroga il server per ottenere le coordinate dei mezzi da mostrare sulla mappa.

- ZonaService: Gestisce il recupero delle informazioni sulle aree operative.

- FlottaService: Invia i comandi di aggiornamento dello stato della flotta

- CorsaService: Invia le richieste di blocco temporaneo o sblocco del veicolo.

- ConfigurazioneService: Richiede al server i parametri di sistema

- RegoleFineCorsaService: Richiede al server quali sono le regole fine corsa e eventuali modifiche.

- SegnalazioneService: Richiede al server la lista delle segnalazioni

- AbbonamentoService: Richiede al server gli abbonamenti disponibili

- OffertaService: richiede al server le offerte del sistema

#### Specifica delle componenti server

Il Server elabora la logica di business, coordina i dati e interagisce con il database. È diviso in 4 strati principali staccati e comunicanti tramite interfacce dedicate.

**<u>CONTROLLER</u>**: Riceve le richieste dal Client tramite l'interfaccia **ClientToServer** e coordina il flusso applicativo verso la Business Logic.

- **AuthController:** Gestisce la sicurezza e l'accesso

  - LoginController: Riceve le credenziali dal client e avvia la procedura di controllo dell'identità.

- **UtenteController:** Coordina le azioni degli utenti standard

  - CorsaController: Riceve le richieste di prenotazione o sblocco del mezzo fatte dall'utente.

  - PagamentoController: Intercetta le richieste di pagamento a fine corsa o all'aggiunta di una carta.

  - HomePageUtenteController: Smista le richieste iniziali dell'utente all'apertura dell'app.

  - AbbonamentoController: Riceve le richieste di sottoscrivere un nuovo abbonamento

  - SegnalazioneUtController: riceve e gestisce le segnalazioni

- **OperatoreController:** Gestisce le operazioni sui mezzi e il territorio

  - MezzoOperatoreController: Gestisce i flussi di inserimento o modifica dello stato dei veicoli inviati dal personale sul campo.

  - ZonaOperatoreController: Gestisce le richieste di creazione e modifica delle zone geografiche e delle relative tariffe/regole.

  - OffertaController: gestisce le richieste di creazione e modifica di offerte e tariffe.

  - DashBoardOPController: gestisce le richieste di estrazione dei dati riguardanti la dashboard

  - ConfigurazioneController: gestisce la richiesta di modifica dei parametri di sistema

  - segnalazioneOPController: gestisce il flusso di visualizzazione e presa in carico delle segnalazioni

  - RegoleFineCorsaController: gestisce le richiesta di modifica delle regole fine corsa

- **AmministrazionePubblicaController:** Gestisce la reportistica istituzionale

  - APController: Gestisce le richieste di estrazione dati e statistiche da parte dei sistemi dell'Amministrazione Pubblica.

**<u>BUSINESS LOGIC LAYER</u>**: Rappresenta il cuore del sistema, dove risiedono le regole di business del software. Comunica con i controller tramite **l'interfaccia BLLToController.**

- ServizioMobilità: Applica le regole per l'avvio e la terminazione di una corsa, lo sblocco fisico del mezzo e il cambio di stato del veicolo.

- ServizioMappa: Elabora i calcoli geografici, verifica se un mezzo si trova all'interno di una determinata area e definisce i confini dei perimetri operativi.

- ServizioUtenti: Contiene la logica per validare le registrazioni, verificare i documenti di guida e modificare i profili.

- ServizioPricing: Calcola la tariffa finale del noleggio in base al tempo, alla distanza e ad eventuali promozioni attive.

- ServizioReport: Aggrega i dati di utilizzo del sistema e genera i file (es. CSV) per il monitoraggio.

- ServizioPrenotazione: Verifica se un mezzo è effettivamente opzionabile e ne gestisce il timer di scadenza della prenotazione.

- ServizioSegnalazione: Contiene la logica per inviare e gestire le segnalazioni

- ServizioOfferta: contiene la logica per la creazione e modifica delle offerte

- ServizioAbbonamento: contiene la logica per la creazione e modifica degli abboanmenti

- ServizioParametri: contiene la logica per impostare i parametri

- ServizioRegoleFineCorsa: contiene la logica per impostare regole fine corsa

**<u>MODEL</u>**: Rappresenta le entità di business del dominio "Smart Mobility". Comunica con la BLL tramite l'interfaccia ModelToBLL.

- Utente: Rappresenta il cliente finale.

- Operatore: Rappresenta il dipendente aziendale con privilegi di gestione flotta.

- RegoleFineCorsa: Contiene i vincoli normativi o aziendali da rispettare per poter chiudere un noleggio (es. foto del parcheggio, zone consentite).

- Mezzo: Rappresenta il singolo veicolo (monopattino, bici, scooter) con targa, ID hardware, livello batteria e coordinate.

- Corsa: Rappresenta la transazione del noleggio (ora inizio, ora fine, mezzo usato, utente, percorso effettuato).

- Zona: Rappresenta un'area geografica poligonale sulla mappa dotata di specifiche regole (es. zona a velocità ridotta, zona di sosta vietata).

- Prenotazione: Rappresenta il blocco temporaneo di un mezzo da parte di un utente prima di iniziare la corsa.

- AmministrazionePubblica: Rappresenta l'ente esterno abilitato alla consultazione dei dati aggregati.

- Pagamento: Rappresenta la ricevuta della transazione economica associata a una corsa o a una penale.

- Tariffa: Modella i costi del servizio (costo al minuto, costo di sblocco, tariffe orarie).

- Promozione: sconto percentuale applicabile a una corsa, con data di scadenza. È un tipo di Offerta — l'utente la seleziona prima del pagamento e riduce l'importo finale.

- Abbonamento: piano a prezzo fisso con durata in giorni (es. mensile), opzionalmente limitato a un tipo di mezzo. Se attivo, azzera il costo di ogni corsa. È anch'esso un tipo di Offerta, sottoscritto dall'utente tramite AbbonamentoUtente.

- ParametriSistema: contiene i valori operativi configurabili del sistema: durata massima prenotazione, periodo di grazia, numero massimo di mezzi per utente, e addebito al minuto durante la pausa corsa.

**<u>DATA ACCESS LAYER</u>**: Fornisce un'astrazione per l'accesso ai dati persistenti, isolando i modelli dal database reale. Comunica con i Modelli tramite l'interfaccia DALToModel. Implementa il pattern Repository

- AttoriRepository: Interroga e salva i dati di Utenti e Operatori.

- MezzoRepository: Gestisce la persistenza e l'aggiornamento dei dati fisici e di stato dei veicoli.

- CorsaRepository: Salva e recupera i dati storici e attivi dei noleggi.

- PrenotazioneRepository: Gestisce il salvataggio sul database delle prenotazioni attive o scadute.

- PagamentoRepository: Registra nel database lo stato delle transazioni (es. pagato, fallito).

- ZonaRepository: Mantiene persistenti le coordinate poligonali delle zone operative.

- TariffaRepository: Gestisce il salvataggio e la storicizzazione dei piani tariffari.

- RegoleFineCorsaRepository: Mantiene persistenti le regole e i vincoli di chiusura corsa nel database.

#### Specifica delle componenti Servizi Esterni

**<u>SERVIZI ESTERNI</u>**: Sottosistema che raggruppa le API di terze parti, connesse tramite l'interfaccia ServiziEsterni.

- ProviderPagamenti: Gestisce la transazione monetaria in sicurezza

- GoogleMaps: Fornisce i servizi di geolocalizzazione, mappe e geofencing

#### Specifica delle componenti Persistenza

Il livello finale di persistenza dei dati, collegato alla DAL tramite l'interfaccia **DALtoDBMS.**

- DBMS: Il sistema di gestione del database che esegue materialmente i comandi.

## Detailed Product Design

### Diagramma delle Classi – Diagramma Generale

<img src="media/image24.png" style="width:6.26806in;height:5.80625in" />

#### Diagramma delle Classi – Client

<img src="media/image25.png" style="width:5.50085in;height:7.96667in" />

#### Diagramma delle Classi – Server

<img src="media/image26.png" style="width:3.98202in;height:8.65833in" />

#### Diagramma delle Classi – View

<img src="media/image27.png" style="width:6.26806in;height:3.21667in" />

#### Diagramma delle Classi – APIService

<img src="media/image28.png" style="width:6.26806in;height:6.36181in" />

#### Diagramma delle Classi – interfacce Client/Server

<img src="media/image29.png" style="width:4.33183in;height:7.29722in" />

#### Diagramma delle Classi – Controller

<img src="media/image30.png" style="width:6.26806in;height:1.77153in" />

#### Diagramma delle Classi – Business Logic Layer

<img src="media/image31.png" style="width:6.26806in;height:2.87083in" />

#### Diagramma delle Classi – Model

<img src="media/image32.png" style="width:6.26806in;height:5.575in" />

#### Diagramma delle Classi – Data Access Layer

<img src="media/image33.png" style="width:6.26806in;height:5.03819in" />

### Specifiche delle Classi

#### Specifica delle Classi – Client

L'architettura è articolata in tre macro-aree:

- **View** — gestisce la presentazione e l'interazione con l'utente.

- **API Service** — gestisce la logica applicativa lato client e la comunicazione con il backend remoto.

- **Interfacce** — definiscono i contratti di comunicazione tra i livelli interni e con il server.

Il Client è esposto come componente unico, suddiviso internamente nei sotto-componenti View e API Service. Le interfacce ApiToView e ServerToClient definiscono rispettivamente il contratto tra View e API Service e tra Client e backend.

##### Panoramica architetturale

Le classi View comunicano con il livello API Service esclusivamente tramite l'interfaccia ApiToView, realizzata dalla classe ApiService. Quest'ultima agisce come façade verso un insieme di service specializzati per dominio (autenticazione, mappa, zone, pagamenti, flotta, reportistica, prenotazioni) e instrada le richieste verso il backend realizzando l'interfaccia ServerToClient.

Questa organizzazione garantisce che:

- le viste non abbiano alcuna conoscenza diretta dei service applicativi né dei dettagli di comunicazione di rete;

- ogni service abbia un perimetro di responsabilità ben definito sul proprio dominio;

- il backend interagisca con il Client tramite un contratto unico e indipendente dalle viste.

##### Interfacce

**1 Interfaccia ClientToServer**

- **Stereotipo:** «interface»

- **Ruolo:** definisce il contratto delle operazioni che il Server espone verso il Client. È realizzata da ApiService lato Client e dal Server lato backend.

- **Ambito funzionale:** autenticazione e gestione del profilo utente, ciclo di vita della corsa (prenotazione, sblocco, terminazione), gestione dei pagamenti, ricerca dei mezzi e caricamento mappa, gestione della flotta, definizione di zone e regole di fine corsa, tariffazione e reportistica.

**2 Interfaccia ApiToView**

- **Stereotipo:** «interface»

- **Ruolo:** definisce il contratto tra View e API Service. È realizzata da ApiService e costituisce il punto di ingresso unico utilizzato dalle viste per richiedere operazioni applicative o aggiornamenti di stato.

- **Ambito funzionale:** autenticazione, prenotazione e gestione della corsa, pagamenti, gestione operativa e amministrativa di mezzi, zone e tariffe, presentazione dei form di accesso e caricamento della mappa.

##### Livello API Service

- **Classe ApiService (Stereotipi:** «Facade», «Singleton»)**:** punto di ingresso unico del livello API Service. Realizza l'interfaccia ApiToView orchestrando le chiamate verso i service specializzati e instrada le richieste verso il Server realizzando l'interfaccia ServerToClient. Si occupa inoltre dell'invio delle richieste HTTP, della gestione delle risposte e della propagazione degli errori alle viste, oltre che della ricezione di notifiche asincrone dal server. Essendo Singleton, garantisce un'unica istanza condivisa tra tutte le viste per l'intera sessione utente.

- **Classe AuthService:** gestisce l'autenticazione dell'utente, la registrazione, la modifica dei dati di account e il mantenimento dello stato di sessione. Espone inoltre la verifica della presenza di una sessione attiva.

- **Classe MapService:** gestisce il caricamento della mappa, l'aggiornamento periodico della posizione dell'utente e la ricerca dei mezzi disponibili nelle vicinanze a partire dalle coordinate correnti.

- **Classe ZonaService**: gestisce la creazione delle zone (operative, vietate, parcheggio) e ne mantiene una cache locale a supporto delle viste cartografiche.

- **Classe PaymentService**: gestisce il portafoglio dell'utente, i metodi di pagamento salvati (incluso il metodo predefinito) e l'esecuzione delle transazioni di pagamento associate alle corse.

- **Classe FlottaService**: gestisce la flotta di mezzi sul lato operatore e amministratore. Si occupa dell'aggiunta di nuovi mezzi, della modifica del loro stato operativo, della dismissione, della verifica di disponibilità, oltre che della gestione delle tariffe e delle regole di fine corsa e del recupero della configurazione corrente di parcheggi e zone.

- **Classe ReportService**: recupera dal backend i dati statistici e i report aggregati a supporto della dashboard dell'amministratore di piattaforma.

- **Classe CorsaService**: gestisce l'intero ciclo di vita della prenotazione, dalla creazione della stessa allo sblocco del mezzo con conseguente avvio della corsa, fino alla terminazione e produzione del riepilogo finale.

- SegnalazioneService: Gestione dell'invio delle segnalazioni di anomalia su un mezzo da parte dell'utente (lato utente). Recupero e gestione dell'elenco delle segnalazioni ricevute a supporto della dashboard operatore (lato operatore).

- AbbonamentoService: Recupero dei piani di abbonamento disponibili pubblicati dall'operatore. Gestione della sottoscrizione di un abbonamento da parte dell'utente e verifica dello stato di sottoscrizione attiva.

- Offerta Service: Recupero delle promozioni/offerte attive a supporto delle viste utente (visualizza promozioni). Gestione della creazione e configurazione di offerte commerciali con condizioni e scadenza (lato operatore).

- ConfigurazoneService: Recupero e impostazione dei parametri numerici di sistema configurabili dall'operatore (durata prenotazione, durata periodo di grazia, numero massimo mezzi per prenotazione di gruppo, addebito pausa corsa, importo bonus).

##### Livello View

Le classi View rappresentano le schermate dell'applicazione. Tutte dialogano con il livello API tramite l'interfaccia ApiToView e sono raggruppate per profilo utente: Utente finale, Operatore e Amministratore pubblica.

###### UTENTE

- VistaAccount: gestisce login, registrazione e recupero credenziali. Costituisce la vista radice dell'applicazione, da cui dipendono funzionalmente tutte le altre viste.

- VistaHomepageUtente: rappresenta la schermata principale dell'utente e visualizza la mappa con i mezzi disponibili nelle vicinanze e le zone definite sul territorio.

- VistaCorsa: gestisce la corsa attiva, dallo sblocco del mezzo alla terminazione. Visualizza informazioni quali durata, distanza e costo, segnala l'ingresso in zone vietate e mostra il riepilogo finale al termine della corsa.

- VistaPrenotazioneMezzo: gestisce la selezione e la prenotazione di un mezzo dalla mappa, mostrando le conferme di prenotazione e segnalando eventuali errori di disponibilità.

- VistaPagamento: gestisce il portafoglio dell'utente, l'aggiunta di nuovi metodi di pagamento e l'esecuzione del pagamento al termine della corsa, mostrando i relativi riepiloghi e conferme.

- VistaSegnalazione: invio di una segnalazione su un mezzo (selezione tipo anomalia, descrizione) con conferma di invio.

- VistaAbbonamenti: consultazione dei piani disponibili e sottoscrizione di un abbonamento, con riepilogo e conferma.

- VistaPromozioni: consultazione delle promozioni/offerte attive applicabili

###### Amministratore Pubblica

- VistaDashboardAP: fornisce la dashboard di reportistica e analisi statistica per l'amministratore, con la possibilità di esportare i dati in formato CSV e PDF.

###### Operatore

- VistaDashboardOperatore: rappresenta la dashboard principale dell'operatore e costituisce il punto di accesso alla mappa operativa con i mezzi gestiti.

- VistaMezziOperatore: consente la gestione completa dei mezzi della flotta, comprendendo la visualizzazione della lista, la modifica dello stato di un mezzo, l'aggiunta di nuovi mezzi e la richiesta di dismissione, con relative conferme e notifiche di esito.

- VistaDefinisciZona: fornisce un editor cartografico per la definizione di nuove zone (parcheggio, operative, vietate), con conferma del perimetro disegnato e possibilità di ritornare in editing in caso di errore.

- VistaImpostazioniRegole: consente la configurazione delle regole di fine corsa, come ad esempio l'obbligo di sosta in determinate zone parcheggio, con relativa conferma di salvataggio.

- VistaTariffePromozioni: gestisce le tariffe e le promozioni applicate ai mezzi, consentendone la visualizzazione e la creazione di nuove tariffe.

- VistaGestioneSegnalazioni: lista delle segnalazioni ricevute, consultazione del dettaglio e pianificazione interventi (integrata o accessibile dalla VistaDashboardOperatore).

- VistaConfigurazioneParametri: configurazione dei parametri numerici di sistema (durata prenotazione, periodo di grazia, numero massimo mezzi, addebito pausa, bonus), con validazione e conferma di salvataggio.

- VistaGestioneUtenti (Operatore): consultazione della lista utenti e sospensione/riattivazione di un account, con conferma e notifica di esito.

##### Relazioni tra le classi

- **Realizzazioni di interfaccia:**

  - ApiService realizza ApiToView (verso il livello View).

  - ApiService realizza ServerToClient lato Client; il Server la usa lato backend.

- **Dipendenze «use»:**

  - AuthService, MapService, ZonaService, PaymentService, FlottaService, ReportService e PrenotazioneService utilizzano ApiService.

  - Tutte le classi Vista\* utilizzano ApiToView.

- **Associazioni tra viste:**

  - VistaAccount è la vista radice; sono ad essa associate VistaHomepageUtente, VistaCorsa, VistaPrenotazioneMezzo, VistaPagamento, VistaMezziOperatore, VistaDashboardOperatore, VistaDashboardAP, VistaDefinisciZona, VistaTariffePromozioni e VistaImpostazioniRegole.

#### Specifica delle Classi – Server

L'architettura server è articolata in quattro macro-aree:

- **Controller** — gestisce la ricezione delle richieste HTTP e la restituzione delle risposte al client.

- **Business Logic Layer (BLL)** — contiene la logica applicativa e di dominio.

- **Model** — rappresenta le entità di dominio del sistema e incapsula lo stato e il comportamento degli oggetti di business.

- **Data Access Layer (DAL)** — gestisce la persistenza e l'accesso ai dati tramite repository.

Il Server è esposto come componente unico, suddiviso internamente nei sotto-componenti Controller, BLL e Model. Le interfacce BLLToController e ModelToBLL definiscono rispettivamente il contratto tra Controller e BLL e tra BLL e Model. L'interfaccia DALtoModel definisce il contratto tra Model e Data Access Layer.

##### Panoramica architetturale

I Controller ricevono le richieste HTTP dal Client e delegano l'elaborazione al livello BLL esclusivamente tramite l'interfaccia BLLToController, realizzata dai service del Business Logic Layer. I service della BLL operano sui modelli di dominio tramite l'interfaccia ModelToBLL e accedono alla persistenza tramite i Repository del Data Access Layer, che realizzano l'interfaccia DALtoModel.

Questa organizzazione garantisce che:

- i Controller non abbiano alcuna conoscenza diretta della logica di business né dei dettagli di accesso ai dati;

- ogni service BLL abbia un perimetro di responsabilità ben definito sul proprio dominio applicativo;

- i Repository costituiscano l'unico punto di accesso al database, isolando il resto del sistema dai dettagli di persistenza.

##### Interfacce

- **Interfaccia ServerToClient**

  - Stereotipo: «interface»

  - Ruolo: Definisce il contratto per l'invio delle richieste dal Client verso il Server. È invocata dall'API Service Layer del client e implementata dai Controller del backend per gestire i dati di input.

  - Ambito funzionale: Inoltro credenziali di accesso, invio comandi del ciclo di corsa (prenotazione, sblocchi, chiusure), trasmissione dati di pagamento, richieste di coordinate per mappe/mezzi, e invio di comandi gestionali dell'operatore (modifica flotta, tariffe, regole e geofencing).

<!-- -->

- **Interfaccia BLLToController**

  - Stereotipo: «interface»

  - Ruolo: definisce il contratto delle operazioni che il livello BLL espone verso i Controller. È realizzata da ServizioMobilità e dagli altri service della BLL.

  - Ambito funzionale: autenticazione e gestione del profilo utente, ciclo di vita della prenotazione e della corsa, gestione dei pagamenti, gestione della flotta di mezzi, definizione di zone e regole di fine corsa, tariffazione e reportistica.

<!-- -->

- **Interfaccia ModelToBLL**

  - Stereotipo: «interface»

  - Ruolo: definisce il contratto tra le entità del Model e il livello BLL. È realizzata dalle classi del Model (Utente, Corsa, Mezzo, Prenotazione, Pagamento, Tariffa, Zona, RegolaFineCorsa).

  - Ambito funzionale: creazione e aggiornamento delle entità di dominio, accesso agli attributi e alle operazioni di business delle singole entità.

<!-- -->

- **Interfaccia DALtoModel**

  - Stereotipo: «interface»

  - Ruolo: definisce il contratto che i Repository devono rispettare per l'accesso al database. È realizzata da tutti i Repository del Data Access Layer.

  - Ambito funzionale: esecuzione di query, aggiornamenti, ricerca per identificatore, ricerca per coordinate e per email.

- **Interfaccia DBMS**

  - Stereotipo: «interface»

  - Ruolo: definisce il contratto di accesso al database relazionale. Espone executeQuery(sql): ResultSet, executeUpdate(sql): int e connettDB().

##### Livello Controller

- **AccountController: Stereotipi:** «FrontController»: è il punto di ingresso unico delle richieste HTTP in ingresso. Gestisce il routing verso i controller specializzati, la gestione centralizzata delle eccezioni e il reindirizzamento in caso di errore.

- **HomePageUtenteController:** gestisce le richieste relative alla homepage dell'utente, tra cui il caricamento della mappa e la visualizzazione dei mezzi disponibili nelle vicinanze.

- **CorsaController:** gestisce il ciclo di vita della prenotazione lato server, dalla creazione della prenotazione allo sblocco del mezzo fino alla terminazione della corsa.

- **PagamentoController:** gestisce le operazioni relative ai metodi di pagamento, tra cui il recupero dei metodi salvati, la creazione di nuovi metodi, la validazione del profilo di pagamento e il calcolo dell'importo finale.

- **DashboardOPController:** gestisce le richieste della dashboard dell'amministratore di piattaforma, fornendo i dati statistici aggregati e la risposta con le informazioni di mappa e reportistica.

- **TariffeController:** gestisce le operazioni CRUD sulle tariffe applicate ai mezzi, esponendo gli endpoint per la creazione, il recupero e la modifica delle tariffe.

- **MezziOperatoreController:** gestisce le operazioni sulla flotta di mezzi lato operatore, tra cui l'aggiunta di nuovi mezzi, la modifica dello stato operativo, la dismissione e la modifica dello stato di un mezzo.

- **ZoneController:** gestisce la creazione, la modifica e il recupero delle zone geografiche (operative, vietate, parcheggio) e delle relative configurazioni cartografiche.

- **AmministrazionePubblicaController:** gestisce le richieste provenienti dall'amministrazione pubblica, in particolare il recupero dei report periodici aggregati.

- SegnalazioneController — gestione delle richieste relative alle segnalazioni: ricezione di una nuova segnalazione (lato utente) e recupero dell'elenco delle segnalazioni (lato operatore).

- AbbonamentoController — gestione delle richieste relative agli abbonamenti: recupero dei piani disponibili, sottoscrizione di un abbonamento e creazione/modifica dei piani (lato operatore).

- OffertaController — operazioni CRUD sulle offerte/promozioni (creazione, recupero, modifica) con condizioni e scadenza configurabili.

- ConfigurazioneController — gestione delle richieste di lettura e aggiornamento dei parametri numerici di sistema.

- AccountUtenteController (Operatore): gestione delle richieste di sospensione e riattivazione dell'account di un utente.

##### Livello Business Logic Layer

- **ServizioMobilità:** orchestratore principale della BLL. Gestisce l'intero ciclo di vita della corsa, la verifica della disponibilità dei mezzi, lo sblocco, la terminazione, il calcolo dell'importo e la gestione delle zone geografiche. Coordina le interazioni tra ServizioMappa, ServizioPagamenti, ServizioPrenotazione e i Repository.

- ServizioMappa**:** gestisce le operazioni geografiche e cartografiche. Si occupa del recupero delle zone attive, della verifica della posizione del mezzo rispetto alle zone consentite e vietate, della validazione della posizione di fine corsa e del caricamento della mappa cartografica.

- **ServizioPagamenti:** gestisce l'autorizzazione dei pagamenti tramite il ProviderPagamenti, la creazione dei record di pagamento, la validazione dei metodi di pagamento e la gestione delle transazioni associate alle corse. Espone inoltre le operazioni di amministrazione degli account di pagamento.

- **ServizioPrenotazione:** gestisce la logica di creazione delle prenotazioni, l'applicazione delle promozioni disponibili e la verifica della scalabilità in termini di disponibilità dei mezzi.

- **ServizioTariffe:** gestisce la logica di tariffazione. Si occupa del recupero delle tariffe applicabili per tipologia di mezzo, della validazione delle tariffe e della promozione delle promozioni attive.

- **ServizioReport:** genera i report statistici aggregati per l'amministratore di piattaforma e per l'amministrazione pubblica, esportando i dati in formato CSV e fornendo le metriche di utilizzo della flotta e dei pagamenti.

- ServizioSegnalazioni — logica di registrazione e recupero delle segnalazioni; associazione della segnalazione al mezzo e all'utente segnalante.

- ServizioOfferte — logica di gestione di promozioni e abbonamenti: validazione delle condizioni e delle scadenze, applicazione delle promozioni attive in fase di tariffazione, gestione della sottoscrizione e del calcolo del bonus.

- ServizioConfigurazione — logica di gestione dei parametri di sistema: validazione dei valori rispetto agli intervalli ammessi e persistenza della configurazione corrente.

- ServizioGestioneUtenti: logica di sospensione e riattivazione dell'account utente, con verifica delle precondizioni e aggiornamento dello stato. Coordinato da Servizio Mobilità.

##### Livello Model

- **Persona:** classe base astratta per tutti gli attori del sistema. Contiene gli attributi comuni di anagrafica (id, nome, cognome, email) e il metodo di login.

- **Utente:** rappresenta l'utente finale del sistema. Estende Persona e mantiene le associazioni con le prenotazioni, i metodi di pagamento e le corse effettuate. Espone le operazioni di modifica del profilo.

- **Operatore:** rappresenta l'operatore di flotta. Estende Persona e ha responsabilità sulla gestione dei mezzi assegnati, sulla modifica dello stato operativo e sulla gestione delle tariffe.

- **AmministrazionePubblica:** rappresenta l'ente pubblico che accede ai report aggregati del sistema. Estende Persona ed espone il metodo di recupero dei report periodici.

- **Mezzo:** rappresenta un mezzo della flotta. Mantiene lo stato operativo (StatoMezzo), le coordinate geografiche correnti, la lunghezza e la StatoDisponibilità. Espone le operazioni di blocco/sblocco e aggiornamento della posizione.

- **Prenotazione:** rappresenta la prenotazione di un mezzo da parte di un utente. Mantiene lo stato della prenotazione (StatoPrenotazione), l'associazione con il mezzo, l'utente e la corsa. Espone il metodo getBiglietto().

- **Corsa:** rappresenta una corsa effettuata da un utente. Mantiene lo stato (StatoCorsa), le date di inizio e fine, il costo calcolato e il percorso. Espone le operazioni getDatiCorsa(), setStato() e creaCorsa(), oltre al metodo di calcolo del costo finale.

- **Pagamento:** rappresenta una transazione di pagamento associata a una corsa. Mantiene l'importo, la data, lo stato (StatoPagamento) e il transactionId. Espone il metodo valida() e crea().

- **MetodoPagamento:** rappresenta un metodo di pagamento salvato dall'utente. Mantiene il tipo (TipoMetodo), il token_esterno e il flag risposta Predefinita. Ha molteplicità 0..\* rispetto all'utente.

- **Tariffa:** rappresenta la struttura tariffaria applicata a un mezzo. Mantiene il tipo di tariffa (TipoTariffa), il costo al minuto, il costo al km e lo stato (StatoTariffa). Espone le operazioni calcolaTariffe() e modificaTariffa().

- **Zona:** rappresenta una zona geografica del sistema (operativa, vietata, parcheggio). Mantiene le coordinate del perimetro, il nome e il tipo (TipoZona). Espone le operazioni di creazione e recupero delle zone figlie.

- **RegolaFineCorsa:** rappresenta una regola che vincola la terminazione della corsa (es. obbligo di sosta in una zona parcheggio). Mantiene l'associazione con la tariffa e la policy applicata. Espone il metodo crea().

- Segnalazione: rappresenta una comunicazione inviata dall'utente all'operatore per notificare un'anomalia su un mezzo (danno, guasto, posizione anomala). Mantiene il tipo di anomalia (TipoAnomalia), la descrizione, la data e lo stato (StatoSegnalazione), ed è associata al mezzo segnalato e all'utente segnalante. Espone il metodo crea().

- Offerta: classe base che rappresenta una politica commerciale configurata e pubblicata dall'operatore. Mantiene nome, descrizione, condizioni, data di scadenza e stato (StatoOfferta). Espone i metodi crea() e verificaValidità().

- Promozione: estende Offerta e rappresenta un'offerta che riduce la tariffa standard (es. sconto percentuale, prime N corse gratis). Mantiene il tipo e il valore dello sconto e viene applicata in fase di tariffazione.

- Abbonamento: estende Offerta e rappresenta un contratto a tempo determinato che garantisce all'utente condizioni tariffarie agevolate o un numero di corse incluse. Mantiene la durata, le corse incluse e la tariffa agevolata, ed è associato agli utenti sottoscrittori.

- ParametriSistema: rappresenta l'insieme dei parametri numerici di configurazione del sistema impostati dall'operatore (durata massima prenotazione, durata periodo di grazia, numero massimo mezzi, addebito pausa, valore bonus). Espone le operazioni di validazione e aggiornamento ed è estendibile con ulteriori parametri.

##### Livello Data Access Layer

- **Repository (Stereotipo:** «Data Access Object») classe base per tutti i repository. Espone le operazioni comuni save(id) e delete(id).

- **UtenteRepository:** gestisce la persistenza degli utenti. Espone le operazioni di ricerca per email, per id e per coordinate, oltre alle operazioni di aggiornamento e cancellazione.

- **MezzoRepository:** gestisce la persistenza dei mezzi. Espone le operazioni di ricerca per tipologia, per stato, per identificativo e per operatore, oltre alle operazioni di aggiornamento e cancellazione.

- **CorsaRepository:** gestisce la persistenza delle corse. Espone le operazioni findById(), findByCorsaId(), update() e delete().

- **PrenotazioneRepository:** gestisce la persistenza delle prenotazioni. Espone le operazioni di ricerca per utente, per mezzo e per stato, oltre alle operazioni di aggiornamento.

- **PagamentoRepository:** gestisce la persistenza dei pagamenti. Espone le operazioni findByCorsaCorsa(), findByElencoId(), update(), save() e delete().

- **TariffeRepository:** gestisce la persistenza delle tariffe. Espone le operazioni di ricerca per tipologia, validazione della configurazione e aggiornamento.

- **ZoneRepository:** gestisce la persistenza delle zone geografiche. Espone le operazioni di ricerca per tipo, per coordinate, per nome e per zona padre, oltre all'aggiornamento.

- **RegolaFineCorsa Repository:** gestisce la persistenza delle regole di fine corsa. Espone le operazioni save(), find(), update() e delete().

- SegnalazioneRepository: gestisce la persistenza delle segnalazioni. Espone le operazioni di ricerca per mezzo, per utente e per stato, oltre alle operazioni di aggiornamento.

- OffertaRepository: gestisce la persistenza delle offerte commerciali (promozioni e abbonamenti). Espone le operazioni di ricerca per tipo, per stato e per scadenza, la validazione della configurazione e l'aggiornamento.

- BonusRepository: gestisce la persistenza dei bonus assegnati agli utenti. Espone le operazioni di ricerca per utente, oltre a save(), update() e delete().

- ParametriSistemaRepository: gestisce la persistenza dei parametri numerici di configurazione del sistema. Espone le operazioni di recupero della configurazione corrente e di aggiornamento.

##### Relazioni tra le classi

**Realizzazioni di interfaccia:**

- ServizioMobilità e i service BLL realizzano BLLToController (verso il livello Controller).

- Le classi del Model realizzano ModelToBLL (verso il livello BLL).

- Tutti i Repository realizzano DALtoModel (verso il Model).

**Dipendenze «use»:**

- Tutti i Controller utilizzano BLLToController.

- ServizioMobilità utilizza ServizioMappa, ServizioPagamenti, ServizioPrenotazione, ServizioTariffe e ServizioReport.

- Tutti i service BLL utilizzano i rispettivi Repository del DAL.

**Associazioni tra classi del Model:**

- Utente ha associazione 0..\* con Prenotazione, MetodoPagamento e Corsa.

- Prenotazione ha associazione 1 con Mezzo e 0..1 con Corsa.

- Corsa ha associazione 1 con Pagamento e 0..1 con RegolaFineCorsa.

- Tariffa ha associazione 0..\* con Mezzo e 1 con RegolaFineCorsa.

- Zona ha associazione 0..\* con Mezzo tramite la verifica della posizione.

### Diagrammi di Sequenza

#### UT - 01 Visualizza Mappa Utente

<img src="media/image34.png" style="width:6.26806in;height:5.52222in" />

#### UT - 02 Prenota Mezzo

#### UT – 03 Sblocca Mezzo

#### UT – 04 Termina Corsa

#### UT – 05 Effettua Pagamento

<img src="media/image35.png" style="width:6.26806in;height:5.50694in" />

#### UT – 06 Salva Metodo di Pagamento

#### UT – 07 Consulta Tariffe

<img src="media/image36.png" style="width:6.26806in;height:3.55903in" />

#### UT – 08 Visualizza Riepilogo Corsa

#### UT - 09 Sospende Corsa

#### UT – 10 Visualizza Promozioni

<img src="media/image37.png" style="width:6.26806in;height:3.49375in" />

#### UT – 11 Visualizza Storico Corsa

#### UT – 12 Invia Segnalazione

#### UT – 13 Sottoscrive Abbonamento

<img src="media/image38.png" style="width:6.26806in;height:6.68125in" />

#### UT – 14 

#### UT – 15 Scrive Recensione

<img src="media/image39.png" style="width:6.26806in;height:4.40208in" />

#### AP – 01 Accede Report

<img src="media/image40.png" style="width:6.26806in;height:3.64444in" />

#### AP – 02 Esporta Report

<img src="media/image41.png" style="width:6.26806in;height:4.08056in" />

#### AP – 03 Visualizza Mappa Amministrazione Pubblica

<img src="media/image42.png" style="width:6.26806in;height:4.17639in" />

#### OP-01 Visualizza Mappa Operatore\
<img src="media/image43.png" style="width:6.26806in;height:3.33125in" />

#### OP – 02 Aggiunge Mezzo

<img src="media/image44.png" style="width:6.26806in;height:4.72292in" />

#### OP – 03 Dismette Mezzo

<img src="media/image45.png" style="width:6.26806in;height:5.13611in" />

#### OP – 04 Modifica Stato Mezzo

#### OP – 05 Definisce Tariffa

<img src="media/image46.png" style="width:6.26806in;height:7.49028in" />

#### OP – 06 Definisce Regole fine corsa

<img src="media/image47.png" style="width:6.26806in;height:5.83125in" />

#### OP – 07 Definisce Zona

<img src="media/image48.png" style="width:6.26806in;height:4.94444in" />

#### OP – 08 Gestisce Segnalazione

<img src="media/image49.png" style="width:6.26806in;height:6.14167in" />

#### OP – 09 Sospende account utente

<img src="media/image50.png" style="width:6.26806in;height:6.51458in" />

#### OP – 10 Definisce Offerta

<img src="media/image51.png" style="width:5.46989in;height:8.80769in" />

#### OP – 11 Configura Parametri Numerici Sistema

<img src="media/image52.png" style="width:6.26806in;height:4.86875in" />

### Note di implementazione — Demo movimento mezzi

- Demo movimento mezzi (helper di presentazione, account demo): `ServizioMappa.aggiornaPosizioneMezzo`
  + endpoint `PATCH /utente/corse/{id}/demo/posizione`, geofencing client-side (`geoUtils.zonaCorrente`),
  mappa operatore in polling. Tracciabilità IF-OP.01 / IF-UT.01 / IF-UT.08.
- Penale fuori zona/vietata nel costo finale: `ServizioPricing.effettua_pagamento(..., penale_fuori_zona)`
  somma `regole_fine_corsa.penale_fuori_zona` all'importo se la corsa transita in zona vietata/fuori
  operativa. Tracciabilità IF-OP.06 (Definisce Regole Fine Corsa) / caso d'uso UT-04.

### Consumo batteria mezzo (comportamento di sistema)

Il livello di batteria (`Mezzo.batteria`) cala con l'uso del mezzo. Implementazione su due livelli,
senza nuove classi (riusa `Mezzo`, `ServizioMobilità`, `ServizioMappa`, repository esistenti):
- **A fine corsa (reale, tutte le corse):** `ServizioMobilità.termina_corsa` decrementa la batteria in
  proporzione alla durata di guida effettiva (`CONSUMO_BATTERIA_PER_MIN = 1.0` punti/min, da
  `CorsaRepository.durata_effettiva_sec`) tramite `MezzoRepository.aggiorna_batteria`. Se la carica scende
  sotto `regole_fine_corsa.batteria_minima` (se configurata) il mezzo va `In manutenzione` invece di
  `Disponibile` (necessita ricarica), altrimenti torna `Disponibile`.
- **Durante la demo (live, visivo):** il calo per-movimento è calcolato dal frontend in base ai km percorsi
  e persistito dall'endpoint demo (campo `batteria` opzionale su `aggiornaPosizioneMezzo`), così cala in
  tempo reale anche sulla mappa Operatore.

Lo stato del mezzo è modificato solo da `ServizioMobilità`. Comportamento legato al ciclo di vita di
`Mezzo` / regole fine corsa (IF-OP.06).

## Data modeling and design

Qui va fornita la specifica di tutti i dati e le informazioni scambiate dal sistema in corso di realizzazione con l’utenza di riferimento e/o gli eventuali altri sistemi con cui esso comunica. Deve essere descritto il modello logico della base di dati e la sua struttura fisica.

### Modello logico del Database

<img src="media/image53.png" style="width:6.26806in;height:3.23194in" />

### Struttura fisica del Database

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

# Glossario

## Acronimi

- **AP**: Amministrazione Pubblica

- **CSV**: Comma-Separated Values

- **NFC**: Near Field Communication

- **OP**: Operatore del Servizio

- **PDF**: Portable Document Format

- **QR**: Quick Response (code)

- **UT**: Utente

- **HTTP**: HyperText Transfer Protocol

- **API**: Application Programming Interface

- **BLL**: Business Logic Layer

- **DAL**: Data Access Layer

- **DBMS**: Database Management System

## Definizioni

- **Account utente**: Insieme di credenziali, dati anagrafici, metodi di pagamento, e-mail, password e storico associati a un utente registrato. Il profilo personale è la vista utente dell'account.

- **Addebito**: Importo economico calcolato al termine di una corsa o di un evento tariffabile e prelevato dal metodo di pagamento associato all'account utente.

- **Amministrazione Pubblica**: Ente locale (comune o equivalente) che monitora l'andamento del servizio di sharing sul territorio e ne analizza i dati aggregati a supporto delle decisioni di pianificazione urbana. Nel sistema è un ruolo distinto da Utente e Operatore, privo di poteri di configurazione diretta della flotta o delle zone.

- **Autonomia residua**: Valore numerico indicante la carica rimasta nella batteria di un mezzo elettrico (e-bike, e-scooter). Espresso in percentuale (%) o in chilometri stimati; l'unità di misura adottata è configurabile dalla piattaforma.

- **Corsa**: Sessione di utilizzo attivo di un mezzo sharing, che inizia con lo sblocco del veicolo e termina con la chiusura della sessione da parte dell'utente. Al termine viene calcolato e addebitato il costo. Sinonimo: Sessione.

- **Fine corsa**: Evento che conclude una corsa; l'esito (valido, penalizzato, rifiutato) dipende dalla posizione del mezzo rispetto a Zona Operativa e Zona di parcheggio.

- **Formato Esportabile:** Formattazione offerta dalla piattaforma per l’esportazione dei dati. Include CSV, PDF.

- **Flotta**: Insieme di tutti i mezzi gestiti da un operatore nell'ambito del servizio di sharing su un determinato territorio.

- **Mappa Operatore**: Visualizzazione cartografica accessibile agli operatori del servizio, che mostra negli ultimi x minuti la posizione e lo stato di tutti i mezzi della flotta, inclusi quelli nascosti alla Mappa Utente. Distinta dalla Mappa Utente per contenuto e permessi di accesso.

- **Mappa Utente**: Visualizzazione cartografica accessibile agli utenti, che mostra i mezzi disponibili con il relativo stato, le varie zone: vietata, limitata, parcheggio e confine operativo. Non mostra i mezzi rimossi dall'operatore.

- **Metodo di pagamento**: Strumento associato all'account utente (carta, wallet, ecc.) utilizzato per regolare gli addebiti.

- **Mezzo**: Qualsiasi veicolo messo a disposizione degli utenti nell'ambito del servizio: bicicletta tradizionale, bicicletta a pedalata assistita (e-bike), monopattino elettrico (e-scooter) e macchina elettrica.

- **Mezzo disponibile:** Mezzo il cui stato (definito nel glossario) è Disponibile, ossia prenotabile da un utente. Gli unici visualizzabili nella Mappa Utente.

- **Operatore del Servizio: Soggetto (azienda privata o consorzio)** responsabile della gestione operativa della flotta e della configurazione della piattaforma: definisce tariffe, promozioni, zone operative, zone soggette a restrizioni e zone di parcheggio parametri di prenotazione e pausa corsa.

- Parametri di sistema: Insieme dei valori numerici configurabili che regolano il funzionamento operativo della piattaforma. Comprendono:

  - la durata massima di una prenotazione,

  - la durata del periodo di grazia per la pausa corsa,

  - il numero massimo di mezzi prenotabili contemporaneamente da un singolo utente

  - l'importo di addebito al minuto applicato durante la pausa corsa al termine del periodo di grazia.

  - Il raggio entro il quale è possibile sbloccare uno o più mezzo

  - Il raggio entro il quale è possibile prenotare più mezzi (il punto di riferimento è il primo mezzo selezionato)

> Tali parametri sono modificabili dall'Operatore tramite l'apposita sezione di configurazione) e si applicano a tutte le operazioni successive alla modifica. *L'insieme dei parametri è aperto a future estensioni: nuovi parametri numerici operativi potranno essere aggiunti senza alterare la struttura del caso d'uso, in quanto condividono la stessa logica di configurazione, validazione e salvataggio.*

- **Pausa corsa**: Stato intermedio di una sessione in cui l'utente blocca temporaneamente il mezzo senza terminare la corsa.

- **Periodo di grazia**: Durata massima configurabile dall'operatore entro cui una pausa corsa non comporta addebiti aggiuntivi o la perdita del mezzo. Se impostato a zero, la funzionalità di pausa gratuita è disabilitata.

- **Prenotazione**: Riserva temporanea di un mezzo specifico effettuata dall'utente prima di raggiungerne fisicamente la posizione. Ha una durata massima configurabile dall'operatore; alla scadenza il mezzo viene automaticamente rilasciato e reso disponibile ad altri utenti.

- **Prenotazione di gruppo**: Prenotazione effettuata da un singolo utente per un numero di mezzi fino al massimo configurato dall'operatore (può anche essere uno).

- **Offerta:** Politica commerciale definita e pubblicata dall'Operatore allo scopo di incentivare l'utilizzo del servizio. È caratterizzata da una denominazione, una data di scadenza, uno stato (attiva, scaduta o in bozza) e da un insieme di condizioni di applicazione. Si specializza nelle seguenti tipologie:

  - **Promozione**: riduce la tariffa standard o introduce condizioni agevolate (ad esempio le prime N corse gratuite o uno sconto percentuale).

  - **Abbonamento**: contratto a tempo determinato (mensile o annuale) che garantisce all'utente condizioni tariffarie agevolate o un numero di corse incluse.

- **Recensione**: Valutazione espressa da un Utente a seguito di almeno una corsa effettuata, accessibile dalla voce "Lascia Recensione" nel menu principale. È composta da un voto numerico (da 1 a 5 stelle) e da un commento testuale facoltativo. Ha lo scopo di raccogliere feedback sull'esperienza d'uso del servizio. Un Utente può lasciare più recensioni nel tempo; non è vincolata a una singola corsa specifica.

- **Regole Fine Corsa**: Insieme di condizioni configurate dall'operatore che determinano l'esito del Fine Corsa. Comprendono: la penale applicata in caso di parcheggio fuori zona, il tipo di vincolo (penale, divieto, avviso) e l'eventuale Bonus riconosciuto all'utente per il parcheggio corretto. La definizione delle regole è separata dalla definizione geografica della Zona di parcheggio.

- **Redistribuzione**: Operazione logistica di spostamento fisico dei mezzi da aree con eccesso di offerta verso aree con carenza, eseguita dal personale operativo sulla base dei dati della Mappa Operatore.

- **Report aggregato**: Documento che consolida statistiche anonime sull'utilizzo del servizio (corse, km, fasce orarie, zone) su un intervallo temporale configurabile. Destinato all'operatore e all'amministrazione pubblica.

- **Riepilogo corsa**: Sintesi presentata all'utente al termine di una corsa, che riporta i dati principali della sessione: durata complessiva, distanza percorsa, costo finale calcolato sulla base della tariffa applicata ed eventuali sconti o bonus. Disponibile anche nello storico corse del profilo utente.

- **Sblocco**: Operazione che disabilita il blocco fisico/elettronico del mezzo, consentendo all'utente di iniziare la corsa. Il metodo di sblocco (QR code, Bluetooth, NFC) è una scelta implementativa.

- **Segnalazione**: Comunicazione inviata dall'utente all'operatore per notificare anomalie su un mezzo (danno fisico, guasto, posizione anomala). Visibile nella Dashboard operatore.

- **Sessione**: Sinonimo di Corsa. Periodo di utilizzo attivo di un mezzo, tracciato dal sistema con marcatura temporale di inizio e fine.

- **Stato (mezzo)**: Condizione operativa corrente di un mezzo. Valori possibili: Disponibile (prenotabile), Prenotato (riservato a un utente), In uso (corsa attiva), In pausa (pausa corsa attiva), In manutenzione (rimosso dalla Mappa Utente), Fuori servizio (bloccato o irrecuperabile).

- **Storico corsa**: L’insieme delle corse effettuate da un Utente.

- **Storico Modifiche**: Registro cronologico delle modifiche apportate dall'Operatore alle configurazioni del servizio, che consente di ricostruirne l'evoluzione nel tempo. Comprende le variazioni a: parametri numerici di sistema, regole di fine corsa, zone operative, tariffe e offerte.

  > *L'insieme delle configurazioni tracciate è aperto a future estensioni: il caso d'uso non cambia, cambia solo a livello implementativo quando una nuova categoria di configurazione viene aggiunta al registro.*

- **Suggerimenti Intelligenti:** Insieme di indicazioni personalizzate prodotte da un servizio esterno di intelligenza artificiale (ServizioAI) a partire dai dati di utilizzo dell'Utente: storico corse, abitudini orarie, zone frequentate, prenotazioni effettuate, abbonamenti attivi e pagamenti. Il ServizioAI valuta autonomamente se i dati disponibili sono sufficienti a produrre indicazioni significative; in caso contrario non genera alcun suggerimento. I suggerimenti possono riguardare l'orario ottimale di prenotazione, la convenienza di un abbonamento rispetto alla tariffa ordinaria, o l'esistenza di promozioni compatibili con le abitudini dell'Utente. La generazione dei suggerimenti non modifica alcuno stato del sistema.

- **Tariffa**: Struttura di pricing applicata a una corsa. La tipologia (es. costo al minuto, alla distanza, tariffa fissa per fascia oraria) è definita e modificabile dall'operatore. La tariffa applicabile è mostrata all'utente prima dell'avvio della corsa.

- **Tariffario**: Elenco pubblicato dall'operatore delle tariffe applicate per ciascuna tipologia di mezzo e modalità di utilizzo. Distinto da Tariffa (struttura applicata alla singola corsa).

- **Utente**: Persona fisica registrata alla piattaforma che utilizza i mezzi di sharing per spostarsi nel contesto urbano. Interagisce con il sistema tramite dispositivo mobile.

- **Zona**:

  - **Zona Operativa**: Perimetro geografico definito dall'operatore entro cui i mezzi della flotta possono circolare e fermarsi. Un mezzo che esce dalla zona operativa può attivare allarmi automatici o bloccarsi. La Zona Limitata e la Zona Vietata hanno sempre la precedenza sulla Zona Operativa.

  - **Zona di parcheggio**: Area geografica designata esclusivamente dall'operatore in cui è consigliato — ma non imposto — parcheggiare il mezzo al termine della corsa. Visibile sulla Mappa Utente. La definizione della zona riguarda esclusivamente il suo perimetro geografico; gli eventuali incentivi associati al parcheggio corretto sono configurati separatamente tramite le Regole Fine Corsa.

  - **Zona Soggetta a restrizioni:**

    - **Zona Limitata**: Area geografica in cui la circolazione dei mezzi è consentita ma con restrizioni configurabili (es. velocità ridotta, orari limitati, divieto di sosta o pausa). Configurata dall’Operatore.

    - **Zona Vietata**: Area geografica definita dall’Operatore in cui la circolazione dei mezzi è completamente vietata. Distinta dalla Zona Limitata (restrizioni parziali). Ha precedenza sulla Zona Operativa in caso di sovrapposizione.
