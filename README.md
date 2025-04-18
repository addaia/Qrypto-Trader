# README

## Abstract

This report evaluates the performance of a Q-learning-based trader (PT2) compared to a deterministic trader (PT1) using intra-day cryptocurrency data. In a frictionless market (idealised), PT2 comfortably outperforms PT1 by a factor of 5 (executing nearly $60$ times more trades in the one day frame used in simulations) even in the occurrence of flash crashes. However, when friction is introduced (e.g. transaction fee), both traders achieve comparable returns, yet PT2's aggressive trading strategy leads to a higher risk profile.

## Introduction

This repository contains a the code used in ACFIM0015 report. Where the following strategies are compared:
- **PT1**: A deterministic trader that follows a fixed set of rules (from DC's BSE)
- **PT2**: A Q-learning-based trader that adapts to market conditions using reinforcement learning.

The simulation explores both idealised frictionless markets and more realistic conditions where transaction fees and other market frictions are present.

## File Descriptions

- `BSE.py`  
  This file is taken from Dave Cliff's BSE. 
  - **Addition of PT2:** The Q-learning-based trader has been integrated.
  - **Real-World Conditions:** Both PT1 and PT2 are now simulated under realistic market conditions. 
  - **Trade Statistics Tweaks:** Minor modifications have been made to how trade statistics and population parameters are calculated, ensuring that the new trader entries are accurately reflected.
 
- **Data Folders**  
  The simulation data is organised into separate folders reflecting different market conditions (data from simulations ran):
  1. **idealised_flash**  
  2. **idealised_plain**  
  3. **realistic_flash**  
  4. **realistic_plain**  

  And the plain (no prefix):
  5. (contains the BTC to USD files used)

    All subdivided into:
     - Downtrend 
     - Sideways  
     - Uptrend

- `functions.py`  
  This file includes the offsets functions (imported from DC's BSE) plus the flash crash offset.


- `***.pdf`  
  Plots.

- `notebook_plotter_results.ipynb` and `notebook_plotter_markettrends.ipynb`
  These files are used to produce the plots from the available data (from folders).

- `notebook_***_simulations.ipynb`  
  Files used to run simulatons (1 per scenario, for a total of 4). 



  

