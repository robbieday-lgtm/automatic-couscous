#Figure 5: Reanalysis vs Weather Stations
#2/27/25

setwd("/Users/robbieday/documents/school/Thesis/ReadyforR")

library(pracma)
library(TTR)
library(matrixStats)
library(matrixStats)
library(zoo)
library(ggplot2)
library(dplyr)

BrP<-read.csv(file="BrnoTuranyCleaned.csv")
TP<-read.csv(file="Telccleaned.csv")
VP<-read.csv(file="Vienna2cleaned.csv")
ZP<-read.csv(file="Znojmocleaned.csv")

dim(Z)

Brcolumnstoaverage <- BrP[, c(5,8,11,14,17,20,23,26,29,32,35)]
Tcolumnstoaverage <- TP[, c(5,8,11,14,17,20,23,26,29,32,35)]
Vcolumnstoaverage <- VP[, c(5,8,11,14,17,20,23,26,29,32,35)]
Zcolumnstoaverage <- ZP[, c(5,8,11,14,17,20,23,26,29,32,35)]

BrA <- rowMeans(Brcolumnstoaverage, na.rm = TRUE)
TA <- rowMeans(Tcolumnstoaverage, na.rm = TRUE)
VA <- rowMeans(Vcolumnstoaverage, na.rm = TRUE)
ZA <- rowMeans(Zcolumnstoaverage, na.rm = TRUE)

Averagesinches <- cbind(VA, BrA, TA, ZA)
Averagesmm <- Averagesinches * 25.4
wsaverage <- rowMeans(Averagesmm, na.rm = TRUE)
length(wsaverage)

RAPrecip <- read.csv("finalarea2013to2023.csv")
column_vector <- as.numeric(Precip[[1]])

n_subsections <- 11  

# Define the length of each subsection
subsection_length <- (5881 - 1417 + 1)  # Calculate length dynamically

# Preallocate a matrix to store the subsections
mat <- matrix(NA, nrow = n_subsections, ncol = subsection_length)

for (i in 1:11){

  start_index <- 1417 + 8760*(i-1)
  end_index <- 5881 + 8760*(i-1)

  subsect <- column_vector[as.numeric(start_index):as.numeric(end_index)]
  
  mat[i, ] <- subsect
  
}

RAaverage <- colMeans(mat)
RAaveragesmoothed <- rollmean(RAaverage, k = 336, fill = NA, align = "center")

plot(1:4465, RAaveragesmoothed, type="l")

RAaverage <- RAaverage * 1000

n_days <- round(length(RAaverage)  / 24)

# Reshape RAaverage into a matrix where each row represents a day (24 hours per row)
RA_matrix <- matrix(RAaverage, nrow = n_days, ncol = 24, byrow = TRUE)

# Sum each row to get daily totals
daily_totals <- rowSums(RA_matrix, na.rm = TRUE)

# Print or use the result
smoothdaily_totals <- rollmean(daily_totals, k = 14, fill = NA, align = "center")

length(smoothdaily_totals) <- 186
length(wsaverage) <- 186

print(smoothdaily_totals)
print(wsaverage)



Precipitation <- cbind(smoothdaily_totals, wsaverage)
matplot(1:186, finalmat, type = "l", col=c("red", "blue"))
legend("topleft", legend = c("Re-Analysis", "Weather Stations"), col = c("red", "blue"), lty = 1, lwd = 2, bg = "white")

difference <- smoothdaily_totals-wsaverage

plot(1:186, difference, type = "l")

t.test(smoothdaily_totals, wsaverage, paired = TRUE)

cor.test(smoothdaily_totals, wsaverage, method = "pearson")


