import json
import sys


class Decode():

    def __init__(self):
        self.transition_prob = dict()
        self.word_to_tag_Dict = dict()
        self.tag2XDict = dict()
        self.emission_prob = dict()
        self.allTags = dict()

    def readData(self):
        with open('hmmmodel.txt', 'r') as f:
            data = json.load(f)


        self.transition_prob  = data["transition_prob"]
        self.word_to_tag_Dict  = data["word_to_tag_Dict"]
        self.emission_prob  = data["emission_prob"]
        self.tag2XDict  = data["tagtoXDict"]
        self.allTags = data["allTags"]

    ###############################################################################

    def ViterbiAlgo(self):


        def getProbability(current_node, trans_prob, emission_prob):
            return  probofNode[graphNodes[current_node]] * trans_prob * emission_prob

        data_path = "/home/sarthak/Mydata/Studies/Spring 2017/NLP/HW/hw5-data-corpus/catalan_corpus_dev_raw.txt"

        with open(data_path) as f:
            sentences = f.readlines()
            for sentence in sentences:
                graphNodes = dict()
                probofNode = dict()
                parent_pointer = dict()

                nodeCount = 0
                #print("\n\nsentence :" , sentence)

                sentenceSplit = sentence.strip("\n").split(" ")
                sentenceSplit = ["##sos##"] + sentenceSplit

                lenSentence = len(sentenceSplit)
                tagFormofSentece = [["Q0"]]
                graphNodes["##sos##" + "/Q0" + "_0"]  = nodeCount
                nodeCount+=1


                ############################### Creating Graph Nodes ###################################################
                try:
                    for i in range(1,len(sentenceSplit)):
                        if(sentenceSplit[i] in self.word_to_tag_Dict):       # if word in existing vocab, get its avail tags
                            tagFormofSentece.append(self.word_to_tag_Dict[sentenceSplit[i]])

                        else:                                                # word not in vocab , get all tags
                            allTags = self.allTags
                            tagFormofSentece.append(allTags)

                        for tag in tagFormofSentece[i]:
                            nodeKey = sentenceSplit[i] + "/"+ tag +"_" +  str(i)
                            if(nodeKey not in graphNodes):
                                graphNodes[nodeKey] = nodeCount              # creating node
                            nodeCount+=1

                except Exception as e:
                    print("exception occurred 1 :", e)

                ##################################### Processing the Graph Nodes #######################################

                try:
                    probofNode[0] = 1
                    for i in range(len(tagFormofSentece) - 1):  # computation is considered in terms of the next word considering the prev word
                        current_word = sentenceSplit[i]
                        next_word = sentenceSplit[i + 1]
                        current_tags = tagFormofSentece[i]
                        next_tags = tagFormofSentece[i + 1]

                        for ctag in current_tags:
                            for ntag in next_tags:
                                tag_tag = ctag + "-" + ntag

                                if (tag_tag in self.transition_prob):
                                    trans_prob = self.transition_prob[tag_tag]
                                else:
                                    trans_prob = 1 / self.tag2XDict[ctag + "-"]  ####################### add 1 smoothing

                                emission_word_tag = next_word + "/" + ntag
                                if (emission_word_tag in self.emission_prob):
                                    emiss_prob = self.emission_prob[emission_word_tag]
                                else:
                                    emiss_prob = 1           ####################### ignoring the emission prob

                                emission_node = emission_word_tag + "_" + str(i + 1)  # a node is represented as eg:flies/NN_2
                                current_node = current_word + "/" + ctag + "_" + str(i)

                                '''
                                1. check if the emission_node already has a prob assigned to it
                                2. if prob already there check if it needs to be updated via some other incoming transition edge
                                '''
                                if (graphNodes[emission_node] not in probofNode):
                                    if (current_node in graphNodes):
                                        probofNode[graphNodes[emission_node]]  = getProbability(current_node, trans_prob, emiss_prob)
                                        parent_pointer[ntag + "_" + str(i + 1)] = ctag + "_" + str(i)

                                else:
                                    current_val = probofNode[graphNodes[emission_node]]
                                    if (current_node in graphNodes):
                                        new_val = getProbability(current_node, trans_prob, emiss_prob)
                                        if (new_val > current_val):
                                            probofNode[graphNodes[emission_node]] = new_val
                                            parent_pointer[ntag + "_" + str(i + 1)] = ctag + "_" + str(i)


                except Exception as e:
                    print("exception 2:", e)

                ############################ Getting the path via Back-pointers #########################


                tagList = self.word_to_tag_Dict[sentenceSplit[lenSentence - 1]]
                for tag in tagList:
                    postags = []
                    key = tag + "_" + str(lenSentence - 1)
                    postags.append(key)
                    while (key in parent_pointer):
                        key = parent_pointer[key]
                        postags.append(key)
                    if (len(postags) == lenSentence):
                        break

                sentenceSplit.pop(0)
                postags.pop()
                postags = list(reversed(postags))

                tagged_sentence = ""
                for i, word in enumerate(sentenceSplit):
                    tagged_sentence = tagged_sentence + word + "/" + postags[i].split("_")[0] + " "

                with open("hmmoutput.txt", 'a') as f:
                    f.write(tagged_sentence + "\n")



def main():
    decoder = Decode()
    decoder.readData()
    decoder.ViterbiAlgo()


if __name__ == "__main__":
    main()