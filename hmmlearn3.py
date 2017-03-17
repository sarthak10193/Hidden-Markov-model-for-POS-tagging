import json
import sys

tagTotalCountDict = dict()          # key : tag, value : #of occurrences of the tag eg NN:56

tag2tagDict = dict()                # key : tag1-tag2 , value : #of occurrences

tagtoXDict = dict()

wordtoTagDict = dict()              # key word, value : all the tags associated  eg time: [NN, VB]

wordTagCountDict = dict()           # used for calculating emissions


def computeTransitionProb(transitionProbDict, tag2TagDict):
    for key, value in tag2tagDict.items():
        transitionProbDict[key] = value/tagtoXDict[key[0:3]]

def computeEmissionProb(wordTagCountDict, emissionProbDict):
    for wordTagKey, value in wordTagCountDict.items():
        emissionProbDict[wordTagKey] = value/tagTotalCountDict[wordTagKey[-2:]]


def main():

    tagDictionary = dict()
    allTags = []
    tagId = 1

    data_path = "/home/sarthak/Mydata/Studies/Spring 2017/NLP/HW/hw5-data-corpus/catalan_corpus_train_tagged.txt"

    with open(data_path) as f:
        sentences = f.readlines()
        for sentence in sentences:
            sentenceSplit = sentence.strip("\n").split(" ")
            for wordtagPair in sentenceSplit:

                currentTag = wordtagPair[-2:]
                currentWord =  wordtagPair[:-3]

                if(wordtagPair not in wordTagCountDict):
                    wordTagCountDict[wordtagPair] =1
                else:
                    wordTagCountDict[wordtagPair] += 1

                if(currentTag not in tagDictionary):
                    tagDictionary[currentTag] = tagId
                    tagId+=1
                    allTags.append(currentTag)

                if (currentTag not in tagTotalCountDict):
                    tagTotalCountDict[currentTag] = 1
                else:
                    tagTotalCountDict[currentTag] += 1

                if(currentWord not in wordtoTagDict):
                    wordtoTagDict[currentWord] = [currentTag]
                else:
                    currentTagset = wordtoTagDict[currentWord]
                    if (currentTag not in currentTagset):
                        currentTagset.append(currentTag)

            for i in range(0,len(sentenceSplit)):
                if(i==0):
                    prevTag="Q0"
                else:
                    prevTag = sentenceSplit[i-1][-2:]

                currTag = sentenceSplit[i][-2:]
                prevCurrentTagTransition = prevTag+"-"+currTag
                prev_to_anyTag_Transition = prevTag + "-"

                if(prevCurrentTagTransition not in tag2tagDict):
                    tag2tagDict[prevCurrentTagTransition] = 1
                else:
                    tag2tagDict[prevCurrentTagTransition] += 1

                if (prev_to_anyTag_Transition not in tagtoXDict):
                    tagtoXDict[prev_to_anyTag_Transition] = 1
                else:
                    tagtoXDict[prev_to_anyTag_Transition] += 1



    ################## Computing the transition prob ###################
    transitionProbDict = dict()
    computeTransitionProb(tag2TagDict=tag2tagDict, transitionProbDict=transitionProbDict)


    ################## Computing Emission ##############################
    emissionProbDict = dict()
    computeEmissionProb(wordTagCountDict =wordTagCountDict, emissionProbDict=emissionProbDict)

    ################## generating the model into a json #################

    with open("hmmmodel.txt", "w") as outfile:
        json.dump({
                   "emission_prob":emissionProbDict,        # key : word/tag , value : emission_prob  ie prob of word given tag
                   "tagtoXDict": tagtoXDict,                # key : tag- , value is the no of tag to any tag transitions
                   "tag2tagDict": tag2tagDict,              # key : tag1-tag2 , value : #of occurrences
                   "transition_prob":transitionProbDict,    # key : tag1-tag2 , transition prob      ie value prob of current tag given prev tag
                   "word_to_tag_Dict":wordtoTagDict,        # key : word , value : the list of tags associated
                   "allTags":allTags,
                   }, outfile, indent=4, ensure_ascii=False)

    print("model written into hmmmodel.txt")



if __name__ == "__main__":
    main()