# British selection algorithm

## How to run with `poetry`

1.	Install Poetry (if not already installed):
Follow the official instructions: [Poetry Installation Guide](https://python-poetry.org/docs/#installation).

2. Install dependencies
`poetry install`

3. Run the script
`poetry run python select_squad.py`

### Setup from scratch to get data (only needed if you want to get the data again for some reason)
```
poetry run python british_download.py
poetry run python download_worlds_data.py
poetry run python calculate_carpinos.py
```

This will get you all the data needed. However the `.csv`s are given in this repo, so you don't need to run.

### What the script does
Scrapes www.openpowerlifting.org for the last 3 years of Classic Results, calculates the carpino scores,
and takes the British results, applies people that won't come, and outputs the squad! The carpino scores are rounded to the nearest 0.5kg.

If you want to play around with who has dispensation (assumed to make the team), and who won't come, then play around with `select_squad.py`.

### Selection formula
1. **Dispensation Athletes**:  
    Athletes granted dispensation are automatically added to the squad.

2. **Carpino Score Priority**:  
    Athletes are selected based on their Carpino scores in ascending order.  
    - Athletes with Carpino scores below 1 are selected first, and so on.

3. **Weight Class Limits**:  
    A maximum of 2 athletes per weight class can be selected for the squad.

4. **Squad Size Limit**:  
    The squad is limited to 8 athletes per gender.

5. **Reserves**:  
    After the main squad is selected, reserves are chosen per gender.  
    - Reserves are selected based on Carpino scores first.  
    - `%WR` is used as a tiebreaker for athletes with no valid Carpino score.

`excluded_names` specifies the people that can't go.

### What is a Carpino Score?

The Carpino score is a calculated metric that compares an athlete’s total to the performance required to secure a top-five placement in the last three years of world-level results.

#### How is the Carpino Score calculated?
* A Carpino score of 0 means the athlete’s total matches or exceeds the average first-place total from the last three years for their weight class.
* A Carpino score between 0 and 1 indicates the athlete’s total is between the average first- and second-place totals.
* A Carpino score between 1 and 2 indicates the athlete’s total is between the average second- and third-place totals.
* Similarly, scores between 2 and 5 reflect how the athlete’s total compares to the averages for third, fourth, and fifth place.
* If an athlete’s total is below the fifth-place average, their Carpino score is recorded as N/A.

#### Example:

If an athlete has a Carpino score of 1.89:
* Their total is between the average second-place and third-place totals.
* Specifically, their total is closer to the third-place average but still better than the second-place average.

This allows selectors to prioritize athletes who are closest to world-class performances when building a competitive squad. Lower Carpino scores indicate stronger performances relative to the historical world-class benchmarks.

## Carpino scores calculated and WRs (from IPF website)
| WeightClassKg | Place 1 | Place 2 | Place 3 | Place 4 | Place 5 | WorldRecord |
|---------------|---------|---------|---------|---------|---------|-------------|
| 59            | 609.0   | 589.0   | 576.0   | 566.5   | 546.5   | 669.5       |
| 66            | 707.5   | 699.5   | 695.0   | 682.5   | 673.5   | 710.5       |
| 74            | 801.5   | 774.5   | 766.0   | 753.5   | 746.0   | 836.0       |
| 83            | 821.0   | 812.0   | 795.0   | 782.5   | 778.5   | 861.0       |
| 93            | 887.0   | 882.5   | 878.0   | 862.5   | 861.5   | 901.0       |
| 105           | 931.0   | 918.5   | 901.5   | 886.0   | 876.5   | 940.5       |
| 120           | 947.5   | 931.0   | 911.0   | 895.0   | 891.5   | 978.5       |
| 120+          | 1071.5  | 1007.0  | 958.5   | 929.0   | 920.0   | 1152.5      |

| WeightClassKg | Place 1 | Place 2 | Place 3 | Place 4 | Place 5 | WorldRecord |
|---------------|---------|---------|---------|---------|---------|-------------|
| 47            | 428.0   | 408.5   | 390.0   | 381.5   | 364.0   | 433.5       |
| 52            | 458.5   | 442.0   | 434.5   | 428.5   | 421.5   | 481.0       |
| 57            | 502.5   | 491.5   | 477.0   | 468.5   | 457.5   | 519.5       |
| 63            | 538.5   | 526.0   | 521.0   | 506.0   | 489.0   | 557.5       |
| 69            | 554.0   | 544.0   | 531.0   | 526.0   | 517.5   | 600.0       |
| 76            | 597.0   | 589.5   | 565.0   | 547.5   | 541.0   | 613.0       |
| 84            | 631.5   | 579.0   | 551.0   | 544.0   | 531.0   | 647.0       |
| 84+           | 697.5   | 680.0   | 663.5   | 644.0   | 629.5   | 731.0       |

## Code quality note
This code was written in ~1 hour mostly by ChatGPT. There's debug logs around etc.

## Team selection as of 2024-12-06
Bear in mind that "Excluded from selection" is just from what I've heard people say. They're "excluded" in terms of
"They said they don't want to go to Euros". No shade.

```
Excluded from seleciton: excluded_names={'Tyri Miller', 'Tony Cliffe', 'Sanchez Dillon', 'Maxwell Gyamfi', 'Jurins Kengamu'}

World's Squad:

M:
  Ade Omisakin (83kg, Total: None, Reason: dispensation)
  Nonso Chinye (120kg, Total: 930.0, Reason: Carpino score 1.05)
  Abdul Majeed Sulayman (120kg, Total: 930.0, Reason: Carpino score 1.05)
  Ajay Sharma #1 (120+kg, Total: 1001.0, Reason: Carpino score 1.12)
  Christian Ayandokun (93kg, Total: 878.5, Reason: Carpino score 1.89)
  Paul Kirkbride-Richards (120+kg, Total: 960.0, Reason: Carpino score 1.97)
  William Pickering #1 (93kg, Total: 840.0, Reason: %WR achieved: 93.23%)
  Ben Pape (105kg, Total: 865.0, Reason: %WR achieved: 91.97%)

F:
  Joy Nnamani (57kg, Total: 506.0, Reason: Carpino score 0.00)
  Ziana Azariah (84kg, Total: 600.0, Reason: Carpino score 0.60)
  Bobbie Butters (57kg, Total: 491.5, Reason: Carpino score 1.00)
  Melina Irawo (84kg, Total: 555.5, Reason: Carpino score 1.84)
  Annie Nelson (69kg, Total: 530.0, Reason: Carpino score 2.20)
  Sabrina Downes (63kg, Total: 487.5, Reason: %WR achieved: 87.44%)
  Sophia Ellis (76kg, Total: 533.0, Reason: %WR achieved: 86.95%)
  Temitope Nuga (76kg, Total: 532.5, Reason: %WR achieved: 86.87%)

Reserves:

M:
  Inderraj Dhillon (120kg, Total: 920.0, Reason: Carpino score 1.55 (Reserve))
  Kibria Ali (66kg, Total: 651.0, Reason: %WR achieved: 91.63% (Reserve))
  Joseph Diva (66kg, Total: 650.5, Reason: %WR achieved: 91.56% (Reserve))
  Owen Hubbard (83kg, Total: 772.5, Reason: %WR achieved: 89.72% (Reserve))

F:
  Adejoke Adetayo (57kg, Total: 478.0, Reason: Carpino score 1.93 (Reserve))
  Makeda Vidal (63kg, Total: 480.5, Reason: %WR achieved: 86.19% (Reserve))
  Bettina Hanlon (76kg, Total: 520.0, Reason: %WR achieved: 84.83% (Reserve))
  Aquinn Onuoha (84+kg, Total: 618.5, Reason: %WR achieved: 84.61% (Reserve))
```
