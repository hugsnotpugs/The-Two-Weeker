setwd("~/Dropbox/Masthead/Descriptions")
load("xkcd data/xkcd_myTdm.RData")
load("xkcd data/xkcd_corpus_temp.RData")  # corpus.temp
library(topicmodels)
library(ggplot2)
library(tm)
library(parallel)
source(file = "wordMap.R")
source(file = "multiplot.R")

############# Removing Sparse Terms ############
myTdm = removeSparseTerms(myTdm, sparse = 0.999)

############## Removing empty docs ##########################
rowTotals <- apply(myTdm, 2, sum)
myTdm = myTdm[,which(rowTotals > 0)]
myDtm = t(myTdm)

corpus.sparse = corpus.temp[which(rowTotals > 0)]

rm(corpus.temp, rowTotals)

############## Latent Dirichlet Allocation/ Gibbs Loglikelihood ###################
numTopics = seq(1, 30)
control_gibbs = list(burnin = 1000, verbose = 0)

## Loglikelihood
loglik = rep(NA, length(numTopics))
for(k in numTopics[2:30]) {
  print(k)
  if(k > 1) {
    lda = LDA(myDtm, k, method = "Gibbs", control = control_gibbs)
    loglik[k] = lda@loglikelihood
  }
}

#save(loglik, file = "lda_gibbs_loglik.RData")
#load(file = "lda_gibbs_loglik.RData")

q_loglik = qplot(x = numTopics, y = loglik, fill = "blue") + 
  geom_line(colour = "blue") + 
  guides(fill = FALSE, color = FALSE) +
  scale_x_continuous(breaks=seq(0,30, by = 5)) + 
  ggtitle("Log-likelihood") + xlab("") + ylab("")+
  theme(axis.text.y=element_text(size=5))

q_loglik


############## Held out Perplexity ###################
held_out_perplexity = function(k, dtm, prob = 0.9) {
  
  control_gibbs = list(burnin = 1000, verbose = 0)
  numDocs = dim(dtm)[1]
  
  # creating testing and training dataset
  test_train = sapply(1:numDocs,function(x) rbinom(1, 1, prob))
  train = which(test_train == 1)
  test = which(test_train == 0)
  lda = LDA(myDtm[train,], k, method = "Gibbs", control = control_gibbs)
  return(perplexity(lda, newdata= myDtm[test,]))
}

numTopics = seq(1, 30)
perplexity_mean = rep(NA, length(numTopics))
perplexity_sd = rep(NA, length(numTopics))

for(k in numTopics[1:30]) {
  print(paste("numTopics",k))
  if(k > 1) {
    perplexity_list = rep(NA, 10)
    for(run in 1:length(perplexity_list)) {
      perplexity_list[run] = held_out_perplexity(k, myDtm) 
    }
    #perplexity_list = mclapply(1:length(perplexity_list), 
    #                           function(x) held_out_perplexity(k, myDtm)))
    
    perplexity_mean[k] = mean(perplexity_list)
    perplexity_sd[k] = sd(perplexity_list)
  }
} 


save(perplexity_mean, file = "lda_gibbs_perplexity2.RData")
#load("lda_gibbs_perplexity.RData")

q_perplex = qplot(x = numTopics, y = perplexity_mean, fill = "blue") + 
  geom_line(colour = "blue") + 
  guides(fill = FALSE, color = FALSE) +
  scale_x_continuous(breaks=seq(0,30, by = 5)) + 
  ggtitle("Held-out Perplexity") + xlab("Number of Topics") + ylab("")
q_perplex
  #geom_errorbar(aes(numTopics, ymin = perplexity_mean - perplexity_sd, 
  #                  ymax = perplexity_mean + perplexity_sd),
  #              size = 0.3, width = 0.2, colour = "darkblue")


########################## Multiplot ########################## 

multiplot(q_loglik, q_perplex)

########################## LDA Final Run ########################## 

k = 15
control_gibbs = list(burnin = 1000, verbose = 1)
lda = LDA(t(myTdm), k, method = "Gibbs", control = control_gibbs)
#save(lda, file = "lda_gibbs2.RData")
load("lda_gibbs2.RData")

########################## Posterior Assesment ########################## 

post = posterior(lda)
setwd("~/Dropbox/Masthead/Descriptions/Graphics/LDA 5")
for(i in 13:15) {
  print(i)
  plotWordPlot(post$terms[i,], min_freq= summary(post$terms[i,])[2], 
                  png_file = paste("t_paired_lda_",i,".png", sep = ""), 
                  width = 1000, height = 750)  #,title = paste("Topic",i))
}

par(mfrow = c(3,5))
for(i in 1:15){
  barplot(post$topics[i,], main = paste("Person",i))
}
inspect(corpus.sparse[15])
