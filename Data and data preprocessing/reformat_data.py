'''
An example of paper: 
#*Some constructions of the join of fuzzy subgroups and certain lattices of fuzzy subgroups with sup property
#@Naseem Ajmal,Aparna Jain
#t2009
#cInformation Sciences: an International Journal
#index498474
#%81430
#%211532
#%225669
#%296731
#%317844
#%417229
#%583404
#%582809
#%596177
#!In this paper, some new lattices of fuzzy substructures are constructed. For a given fuzzy set @m in a group G, a fuzzy subgroup S(@m) generated by @m is defined which helps to establish that the set L"s of all fuzzy subgroups with sup property constitutes a lattice. Consequently, many other sublattices of the lattice L of all fuzzy subgroups of G like L"s"""t,L"s"""n,L"s"""n"""""""t, etc. are also obtained. The notion of infimum is used to construct a fuzzy subgroup i(@m) generated by a given fuzzy set @m, in contrast to the usual practice of using supremum. In the process a new fuzzy subgroup i(@m)^* is defined which we shall call a shadow fuzzy subgroup of @m. It is established that if @m has inf property, then i(@m)^* also has this property.
'''

class Data_Reformat: 
    def __init__(self, text_file='outputacm.txt'):
        self.f = open(text_file,encoding='utf-8')
        self.num_paper = None
        # Create databases here
        self.papers = [] #list of list of strings with paper information
        self.authorship = []
        self.citation = []
        self.paper_info = []
        self.abstract =[]

    def separate_paper(self):
        line = self.f.readline()   # include newline
        line_index = 1
        single_paper = []

        while line:
            line = line.rstrip()  # strip trailing spaces and newline

            if line_index == 1 :
                self.num_paper = int(line) 
            else:
                if line !="":
                    single_paper.append(line)
                else: 
                    self.papers.append(single_paper)
                    single_paper = []

            line = self.f.readline()
            line_index +=1

    def fill_table(self):
        assert self.papers!=[], f"You forget to run separate_papers(): {self.papers}"        
        assert self.num_paper == len(self.papers)
        for paper in self.papers: 
            '''
            assert paper[0][0:2]=="#*", f"oh no! title doesn't start with #*: {paper[0][0:2]}"
            assert paper[1][0:2]=="#@", f"on no! author doesn't start with #@:{paper[1][0:2]}"
            assert paper[2][0:2]=="#t"
            assert paper[3][0:2]=="#c"
            assert paper[4][0:6]=="#index"
            '''
            title = paper[0][2:]
            author_list = paper[1][2:].split(",")
            year = int(paper[2][2:])
            conference = paper[3][2:] #might be empty string ""
            index = int(paper[4][6:])

            self.paper_info.append([index,title,year,conference])

            for author in author_list:
                self.authorship.append([index,author.strip()])

            paper_info_length = len(paper)
            if paper_info_length >5:
                for i in range(5, paper_info_length):
                    if paper[i][0:2]== "#!": #abstract 
                        self.abstract.append([index, paper[i][2:] ])
                    elif paper[i][0:2]== "#%": #citation 
                        self.citation.append([index,int(paper[i][2:])])
                    else:
                        print(paper[i])

        print("Number of papers we have information on: ", len(self.paper_info))
        print("There are in total of %s authors."%str(len(self.authorship)))
        print("There are in total of %s citations."%str(len(self.citation)))
        print("There are in total of %s abstract."%str(len(self.abstract)))
        assert self.authorship != []
        assert self.citation != []
        assert self.paper_info != []
        assert self.abstract !=[]

        return self.paper_info, self.authorship, self.citation, self.abstract

acm_reformater = Data_Reformat()
acm_reformater.separate_paper()
paper_info, authorship, citation,absrtact = acm_reformater.fill_table()

#then we can import those to sql or other platform if needed 