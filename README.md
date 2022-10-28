# Licence Plate Recognition & Detection
## TOTAR - Tam Otonom Mobil Radar Sistemi
#### _Tübitak 2209-A Projesi_
> Not: Tüm sistem Jetson Nano 4 GB üzerinde çalıştırılmıştır.

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Bu projenin asıl amacı olan radar hız denetleme sistemlerini tam otonom hale getirmektir. Şu anda mobil radar hız denetleme sistemleri kamera ve radar yardımıyla plaka ve hız verisi elde edildikten sonra bir memur tarafından el ile makbuz kesilerek ceza yazılmaktadır. Bu proje gerek insan yükünü azaltmak gerek uluşabilecek aksaklıkların ve hataların önüne geçmek için kullanılması amaçlanmaktadır. 

Bu araştırma projesi sayesinde gelişen teknolojiyle beraber akıllı hale gelen şehirleşmelerde insan yükünü azaltarak ve işlemleri otomatize bir şekilde bilgisayara devrederek teknolojiye ayak uydurulacaktır. Ayrıca oluşabilecek teknik hataların önüne geçilerek sistem ve çalışan birey kaynaklı kaçak geçişler en aza indirilecektir. Çalışan sistemle beraber elde edilen veriler anlık olarak localde oluşturulan web arayüze aktarılmaktadır.

## Features

- Özgün veri setiyle eğitilmiş YOLOv5 modeli ile plaka tespiti
- OCR tekniği ile plaka anlamlandırma
- Flask ile web arayüzü ve veri görselleştirme
- Tespit edilen tüm araçların görsel olarak kayıt altında tutulması
- Jetson Nano Linux altyapsı

## Scripts Detail
3 ayrı script olarak çalıştırılan bu sistemde 3 farklı Python sürümü kullanılmıştır.
Python3.7.1 ve Python3.8.10 versiyonları Jetson Nano ile uyumlu Anaconda üzerinde environment oluşturarak kurulmuştur.
| Script | Python Version | File to Run |
| ------ | ------ | ------ |
| Object Detection | [Python3.6.9](https://www.python.org/downloads/release/python-369/) | totar.py |
| Tesseract OCR | [Python3.7.1](https://www.python.org/downloads/release/python-371/) | MainProcess.py |
| Web Dashboard | [Python3.8.10](https://www.python.org/downloads/release/python-3810/) | web/run.py |

### Database
Kullanıcı ve tespit edile araç plakaları 2 ayrı SQL tablosunda tutulmaktadır. Database olarak SQLite3 kullanılmıştır.

### Hardware
> Jetson Nano 4 GB
> Raspberry Pi Camera V2
> Arduino Uno
> Ublox Neo6M GPS Module
> DHT11 Temprature Sensor
> 1.8" RGB TFT Display

### Bazı Görseller
