# Netrunner: Agendas and Accesses

## Description
Netrunner is a two player competitive card game supported by [Null Signal Games](https://nullsignal.games/) where players take on the role of a corporation or runner (hacker) in a dystopian cyberpunk setting. Before a game begins each player constructs their own unique deck by choosing which cards to include from a pool of available cards. The corporation's goal is to play, advance, and score agenda cards that are protected by ice (Intrusion Countermeasures Electronics). The runner's goal is to steal agenda cards by getting past the corporation's ice in order to access cards in the corporation's deck. When runners access cards they often do so with limited or no information about what card they will be accessing, meaning that when runners access a card they have a semi-random chance of accessing an agenda they can steal. Depending on the odds of accessing an agenda and the value of the agenda the runner will need to make a certain number of accesses during a game to steal the 7 agenda points they need to win the game. I am calling the average number of unique accesses a runner needs to win against a corporation deck the access threshold for that deck. In this study I will be looking at how deckbuilding decisions affect the access threshold.


## Goal

**The goal of this project is to determine the effect of different deckbuilding decisions on access threshold**

I have 4 research questions in mind for this study.

1) What is the effect of agenda density (number of agenda points in a deck relative to the total number of cards) on access threshold?

2) What is the effect of agenda concentration (how concentrated the agenda points are among the agenda cards in a deck) on access threshold?

3) What is the effect of Let Them Dream agendas on access threshold?

4) What deck building recommendations can I make based on my findings?

[**Click Here for the Full Analysis**](https://github.com/Johndsalas/Netrunner-Analysis/blob/main/netrunner_agendas_and_accesses.ipynb)

## Analysis Methodology

* Develop a constructed matrix of combinations of minimum deck size, use of the four card margin, agenda point total, and distribution of 1, 2, and 3 point agendas for corporation decks
* Each feature is represented as a column in a dataframe and each row represents one unique combination of these features
* Add additional rows to the matrix by replacing the maximum number of normal two-point agendas with Let Them Dream agendas
* Calculate access threshold for each row using digital experiments
* Examine how different feature values shift the possibility matrix to determine the effect of those features on access threshold

## Methodology of Digital Experiments to Determine Access Threshold

* Access threshold is the average number of unique random accesses a runner needs to steal 7 points worth of agendas and win the game
* The access threshold of each combination of features or row was calculated using the following method
   * Represent the corporation's deck by making a list containing a number of values equal to the testing deck’s deck size
       *  Values in the list represent the agenda point values of the agendas in the deck
           *  Mostly zeros with a number of one, two, and three values equal to the number of one, two, and three point agendas in the deck
   * Simulate a random access by choosing a value at random from the list and adding that value to the runners total score
   * Simulate the accessed card being stolen, trashed (discarded from play), or otherwise avoided by removing that card from the list
   * Continue simulating random accesses until the runner has a score of 7 or more and count the number of accesses it took to reach this total
   * To ensure a large sample size and reduce statistical error repeat the experiment 100,000 times and get the average result
   * Round result to the nearest whole number for ease of discussion and communicability of result

## Let Them Dream Methodology

* Let Them Dream is a two-point agenda with an ability that reduces its value by 1 if it is in the runner's score area effectively making it a two-point agenda for the corporation and a one-point agenda for the runner
* To measure the impact of Let Them Dream agendas on access threshold additional rows were added to simulate replacing ‘normal’ two-point agendas with maximum allowable number of ‘Let Them Dream’ agendas
   * For each row with one or more two-point agendas an additional row was added replacing up to a maximum of three two-point agendas with Let Them Dream Agendas
   * A maximum of 3 replacements are made because the maximum number of card copies (by title) that can be included in a deck is 3
   * A replacement is simulated by lowering the number of two-point agendas by one and increasing the number of one-point agendas by one
   * This effectively counts the agenda as being worth 2 points for agenda point total and 1 point if the runner steals the agenda
   <br>
* **Limitation**
   * This matrix only includes possibilities replacing the maximum number normal two-point agendas
       * It does not account for replacing less than the maximum (Example has 2 two-point agendas but only replaces one)
       * It does not account for replacements swapping 2 one-point agendas for 1 Let Them Dream
       * It does not account for replacements swapping 1 three-point agenda for 1 one-point agenda and 1 Let Them Dream

## Data Dictionary

|Feature|Definition|
|---|---|
|Deck Size| Count of cards in the deck|
|Agenda Points| Total value of all agenda points on agendas |
|Agenda Count| count of agendas |
|One-Point Agendas| Count of agendas with a value of 1 |
|Two-Point Agendas| Count of agendas with a value of 2 |
|Three-Point Agendas| Count of agendas with a value of 3 |
|LTD Count| Count of "Let Them Dream" agendas |
|Agenda Density| Agenda Points Divided by Deck Size |
|Access Threshold| Average number of unique blind accesses the runner needs to win the game |

## Lexicon
|Term | Definition |
|---|---|
|Runner | The player playing the runner |
|Corporation or Corp | The player playing the corporation |
|Build | A particular set of cards chosen for a player's deck |
| Let Them Dream | Title of an agenda card, This card counts as a two-point agenda for the corporation but only gives the runner 1 point if it is stolen |
|Unique Blind Access| When the runner accesses an unknown card for the first time |
| Agenda Density | The number of agenda points in a deck relative to the number of cards |
|Agenda Concentration | The degree to which agenda points are concentrated in high point cards |

## Summary of Findings

Overall this study provides a framework for understanding the impact deckbuilding decisions have on access threshold. The range of impact is much smaller than I originally thought. This limited range of impact indicates that access threshold should be deprioritised in favor of including cards that are more synergistic to a given build. Still, knowing what to deprioritise, when deckbuilding, is valuable information. Additionally, in cases where decisions have little or no effect on synergy, such as using the 4 card margin and choosing between cards of comparable synergy selecting the option that increases access threshold will grant an advantage. This study also provides 'receipts' for commonly given deckbuilding advice. It confirms and, in many cases, quantifies the impact of these suggestions. Below are specific findings and recommendations.

**General**
* Access thresholds across the constructed matrix have a range of 14 to 20 meaning that deck building decisions have a 6 access influence on access threshold
* Agenda density has a negative relationship on access threshold
* Builds with a higher concentration of agenda points have higher access thresholds
* Agenda density has a stronger effect on access threshold than agenda concentration

**Agenda Density**
* Choice of minimum deck size has a negligible effect on access threshold
* The 4 card margin increases access threshold by about 1-2 accesses
* Builds using the minimum agenda point total have an access threshold of about 1 access higher than builds including an extra agenda point  

**Agenda Concentration**
* There is a negative relationship between agenda count and access threshold setting a range of 2-4 possible values
* There is a small positive relationship between three-point agenda count and access threshold
* There is a small negative relationship between one-point agenda count and access threshold

**Let Them Dream**
* Replacing normal 2-point agendas with Let Them Dream agendas will increase access threshold by about 1 access per replacement

## Recommendations

**Consider Access Threshold as a Factor when Optimizing a Build not as Major Focus**
* Access threshold has a range of 6 accesses that are determined through deck building decisions with most normal builds falling between 15 and 17. This limits the potential impact of optimizing for access threshold.
* A higher access threshold will help you edge out victories in games with competitive boardstates, however making the runner access a few extra cards is unlikely to turn the tide if your boardstate is poor

**Use the 4 Card Margin and Build to the Lower Agenda Point Total**
* Using the 4 card margin will increase your access threshold by 1-2 accesses while granting you additional resources
   * The cost of slightly reduced consistency due to the increased deck size is usually negligible
* Using the minimum number of agenda points will increase your access threshold by about 1 access compared to builds that include an extra agenda point

**Use High Value Agenda Cards Where it Will not Disrupt the Deck's Synergy**
* Higher value agendas slightly increase access threshold and open additional deckbuilding slots by concentrating agenda points in one card
* Higher point agendas can also be harder to score 
* Carefully consider how your build is going to score high point agendas before including them

**Strongly Consider Including Let Them Dream in your Build**
* Replacing normal 2-point agendas with Let Them Dream agendas will increase access threshold by about 1 access per replacement
   * It effectively lowers the number of agenda points available for the runner to steal by 1 per inclusion
   * Its ability also allows you to 'shuffle away' agendas from HQ and 'hide' high point agendas on the bottom of R&D further reducing the odds of the runner stealing an agenda during a blind access
* There are reasons not to include Let Them Dream in your build
   * The card is neutral and cost 1 influence per copy in any deck it is included in
   * It competes for deck slots with other agendas that might provide more synergy

## Steps to Reproduce
You will need access to the following python libraries:
* Pandas
* Seaborn
* Matplotlib
* Regex
* Warnings

1) Clone this repository
2) (Optional) If you would like to generate your own corporation deck matrix
   * Delete agenda_matrix.xlsx from cloned repository
   * Run get_agenda_matrix.py to generate a new agenda_matrix.xlsx
       * Deleting the old file first instead of overriding gives a visual indicator that get_agenda_matrix.py has run correctly due to the appearance of a new file
       * **Digital Experiments are UNSEEDED** your results may vary slightly
           * this is unlikely due to the large sample size of the experiments
3) Run notebook
   * you will need notebook_companion.py in the same file in order to run the notebook

## Next Steps
* Develop a more robust version of the possibility matrix for builds including Let Them Dream agendas expanding from the 2-point agenda replacements to all possible builds
 * Develop a deeper understanding of the amount of impact changes in agenda concentration have on access threshold
   * Develop a better metric for understanding agenda concentration across all possible builds
       *  possible metric could include total agenda points / count of agendas
* Examine changes across multiple features to determine how changes in one feature may affect changes in another feature in regard to their effect on access threshold