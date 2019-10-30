library(jsonlite)
# library(tidyjson)

f <- "~/Downloads/canvas live event sample"

raw <- readLines(f)

# split with:  {\"sensor\"  ? -not easily since the thing starts with that
(split.raw <- unlist(strsplit(raw, "(?<=\\}\\]\\})", perl = T)))
(jraw <- lapply(split.raw, (function(x) fromJSON(x))))
jraw[[1]]$data
jdf <- lapply(jraw, function(x) as.data.frame(x$data))


d <- fromJSON(split.raw[1], simplifyDataFrame = T)
m <- fromJSON(split.raw[1], simplifyDataFrame = T, flatten = T)
# m <- m$data
# d <- d$data

# `m` is what we want

unm <- as.data.frame(unlist(m))
unm <- as.data.frame(t(unlist(m)))      # there we go

ldat <- lapply(jraw, function(x) as.data.frame(t(unlist(x))))


# Try embiggen ------------------------------------------------------------

rm(list = ls())
gc()

raw <- readLines("~/Downloads/canvas-live-events-1-2018-05-01-00-01-26-bfb4cbb5-abd1-4444-ae3f-64c2df0e7112")
spt.raw <- unlist(strsplit(raw, "(?<=\\}\\]\\})", perl= T))
js.raw <- lapply(spt.raw, function(x) fromJSON(x, simplifyDataFrame = T, flatten = T))
df.ls <- lapply(js.raw, function(x) as.data.frame(t(unlist(x))))

# sizes
table(unlist(lapply(df.ls, dim)))

# test - find actions:
i <- sapply(df.ls, function(x) x$data.action)
table(i)

# split by `var`
# actually i need an index for the actual list elements, not a variable w/in each
# to wit: `i`
spt.type <- split(df.ls, i)

# and there we are - find a value/factor/element and split or otherwise extract elements from the list of entries