## Gap Statistic
library(parallel)
library(skmeans)
library(lsa)

### Calculates within ss of uniformly distributed samples after clustering ####
Uniform_WithinSS = function(k, data, type) {
  unif = apply(data, 2, function(x) runif(length(x), min = min(x), max = max(x)))
  if(type == "cosine") {
    kmeansResult = skmeans(unif, k)
    withinSS = withinClusterScatterCosine(kmeansResult, unif)
  } else {
    kmeansResult = kmeans(unif, k, iter.max=30)
    withinSS = sum(kmeansResult$withinss)
  }
  return(withinSS)
}


### Calculates the gap statistic for Spherical Clustering for a sequence of clusters ####
calcGapCosine = function(cluster_seq, data) {
  gap_vec = rep(NA, length(cluster_seq))
  gap_mean = rep(NA, length(cluster_seq))
  gap_sd = rep(NA, length(cluster_seq))
  gap_within_data = rep(NA, length(cluster_seq))
  
  for(k in cluster_seq) {
    print(paste("Starting k ", k))

    W_unif_list = c()
    
    system.time( for(gd_run in 1:1) {
      print(paste("uniform_run", gd_run))
      W_unif = mclapply(seq(1,2, by = 1), function(x) Uniform_WithinSS(k, data, "cosine"))
      ## Unlist the vectors if necessary
      if(is.vector(W_unif)){ W_unif = unlist(W_unif) }
      W_unif_list = c(W_unif_list, W_unif)
    }  )
    print("on true data")
    kmeansResult = skmeans(data, k, control = list(nruns = 50))
    withinssData = withinClusterScatterCosine(kmeansResult, data)
    gap_within_data[k] = log(withinssData) 
    gap = mean(log(W_unif)) - log(withinssData) 
    #print(paste("gap statistic:", gap))
    gap_vec[k] = gap
    
    gap_mean[which(cluster_seq == k)] = mean(log(W_unif_list))
    gap_sd[which(cluster_seq == k)] = sd(log(W_unif_list))
  }
  gap = as.data.frame(cbind(gap_vec, gap_sd, gap_mean))
  colnames(gap) = c("Gap", "Gap_sd", "Gap_mean")
  return(gap)
}

calcGapEuclid = function(maxClusters, data) {
  gap_vec = rep(NA, maxClusters)
  gap_sd = rep(NA, maxClusters)
  
  for(k in seq(1, maxClusters, sep = 1)) {
    print(k)
    W_unif = mclapply(seq(1,5), function(x) Uniform_WithinSS(k, data, "euclidean"))
    kmeansResult = kmeans(data, k, iter.max=30)
    gap = mean(log(W_unif)) - log(sum(kmeansResult$withinss))
    gap_vec[k] = gap
    gap_sd[k] = sd(log(W_unif))
  }
  gap = as.data.frame(cbind(gap_vec, gap_sd))
  colnames(gap) = c("Gap", "Gap_sd")
  return(gap)
}


plot_gap_statistic = function(gaps, stddevs, num_clusters) {
  qplot(num_clusters, gaps, xlab = "# clusters", ylab = "gap", geom = "line", 
        main = "Estimating the number of clusters via the gap statistic") + 
    geom_errorbar(aes(num_clusters, ymin = gaps - stddevs, ymax = gaps + stddevs), 
                  size = 0.3, width = 0.2, colour = "darkblue") + 
    scale_x_continuous(breaks=num_clusters)
}
