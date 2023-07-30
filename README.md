# Money-is-Motivation by Matthew Senick

Read the paper [here](https://Matts52.github.io/assets/papers/Money_is_Motivation.pdf)

### Overview

This project serves as the codebase for the generation and analysis of the short-term predictive value of effective intrateam salary dispersion metrics with respect to firm outcome performance indicators. In the following analysis, teams in the NBA are used as a natural experiment for this relationship. Essentially, the full project can be seen as two distinct stages. First off, we have the scraping and data collection stage, whereby salary, game-by-game floor minute statistics, and game results are gathered. Using these scraped statistics, game and season-level dispersion metrics are generated, which are then associated with each game. For the second stage, random forest models are built to study the predictive capacity of salary dispersion on game-level outcomes. As input, average salary per minute of game-time, salary variance per minute of game time, gini coefficient, herfindahl index, and the maximum salary of a palyer on the team are used as input. As output, binary win/loss results, relative point total, and home/away point totals are all used as response variables of the model. In the end, it is determined however, that there is no significant short-term predictive value when using this proxy of the NBA. Interpreting this, it is concluded that effective salary dispersion has no predictive effect on short-term competitive firm perfomance.

### Conclusion

I learned a lot from writing this paper. First and foremost, I learned the amount of care that goes into writing a legitimate economics paper. Additionally, this served as a first taste into intensive web scraping procedures for an academic paper, which also humbled me. This being one of my first glances into economic research was a tremendous stepping stone that I am very proud of, regardless of the significance of the results contained within. Lastly, this was my first look at utilizing Machine Learning models in R, as I was still utilizing (prehistoric) Weka and occasionally scikit-learn before this paper.
