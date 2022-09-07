

import re
import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
Plus_Minus = '+-'
Mul_Div_Mod = '*/%'
Compound = ['+=', '*=', '-=', '/=', '%=']
Relational_Operation = ['<', '>', '<=', '>=', '!=', '==']
And_Logical = ['&&']
OR_Logical = ['||']
Brackets = ['(', ')', 'open', 'close', '[', ']']
Key_words = ['bool', 'char', 'int', 'double', 'private', 'protected', 'final', 'try', 'catch', 'finally', 'throw', 'break', 'case', 'continue', 'while', 'range', 'switch',
             'if', 'else', 'extends','string', 'implements', 'instanceOf', 'new', 'return', 'interface', 'this', 'throws', 'void', 'super', 'accept', 'decline', "null", 'def', 'open', 'close', 'const','main']
punctuators =[',',':',';','.']
id = r'^[A-Za-z_]+[A-Za-z0-9_]*'



# Error reporting


class Error:
    def __init__(self, position_start, position_end, error_name, details):
        self.position_start = position_start
        self.position_end = position_end
        self.error_name = error_name
        self.details = details

    # return error as string

    def asString(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.position_start.file_name}, line {self.position_start.line + 1}'
        f = open(
            r'./token.txt', 'a')
        f.write(
            f'({self.error_name},{self.details},{self.position_start.line})\n')
        return result

    # for not allowed characters


class IllegalCharError(Error):
    def __init__(self, position_start, position_end, details):
        super().__init__(position_start, position_end, 'Illegal Character', details)

class Position:
    def __init__(self, index, line, column, file_name, file_txt):
        self.index= index
        self.line= line
        self.column= column
        self.file_name= file_name
        self.file_txt = file_txt
    #creating method
    def next_pos(self, current_char):
        self.index += 1
        self.column +=1

        if current_char == '\n':
            self.line +=1
            self.column = 0
        
        return self

    def duplicate(self):
        return Position(self.index,self.line,self.column,self.file_na,me,self.file_txt)

#creating token 
class Token:
    def __init__(self, class_part, value = None, line_no = None):
        self.class_part = class_part
        self.value = value
        self.line_no = line_no

    def __repr__(self): #use to return obj in string representation 
        if self.value:
            return f'{self.type}:{self.value}:line{self.line}'
        return f'{self.type}:line{self.line}'

class lexeical:
    def __init__(self, file_name, txt):
        self.file_name=file_name
        self.txt= txt
        self.position = Position(-1 ,0, -1, file_name, txt)
        self.current_char = None
        self.next_pos()

    def next_pos(self):
        self.position.next_pos(self.current_char)
        
        if self.position.index < len(self.txt):
            self.current_char = self.txt[self.position.index]
        else:
            self.txt = None
    
    #token generate and save it into file
    def createTokens(self):
        token=[]
        while(self.current_char != None):
            postion_start = self.position.duplicate()

            if self.current_char in ' \t':
                self.next_pos()  
            elif self.current_char in re.findall('\w',self.current_char):
                token.append(self.isIdentifier())
            elif self.current_char == "'":
                token.append(self.isChar())   
            elif self.current_char == '"':
                token.append(self.isString())
            
            elif self.current_char == '#':  # checking whether comment is single line or multi line comment
                token.append(self.CommentChecker())

            elif self.current_char in re.finadall('\d',self.current_char):
                token.append(self.isNum())
            elif self.current_char in Compound: 
                token.append(self.isCompound())
                self.next_pos()    
            elif self.current_char in Plus_Minus:
                token.append(self.isPM())
                self.next_pos()
            elif self.current_char in Mul_Div_Mod:
                token.append(isMDM())
                self.next_pos()
            elif self.current_char in Brackets:
                token.append(isBra())
                self.next_pos()
            elif self.current_char in Relational_Operation:
                token.append(self.isRO())
                self.next_pos
            else:
                self.next_pos()
                IllegalCharError(position_start, self.position, "'" + char + "'")
        return token,None 
                
    def isIdentifier(self):
        a = open(
            r'./token,txt','a'
        )
        id_str = ""
        position_start = self.position.duplicate()

        while self.current_char != None and self.current_char in re.findall(id,self.current_char):
            id_str += self.current_char
            self.next_pos()

        if id_str in Key_words:
            token_type = 'Keyword'
        else:
            token_type = 'Identifier'
        f.write(f'({token_type},{id_str},{self.postion.line+1})')
        return token(token_type,id_str,self.position.line+1)
    
    def isString(self):
        a = open(
            r'./token,txt','a'
        )
        string = ''
        position_start = self.position.duplicate()
        
        self.next_pos()

        escape_chars = {
            'n' : '\n'
            't' : '\t'
        }
        while self.current_char != None and (self.current_char != '"'):
            if escape_char:
                string = string + escape_chars.get(self.current_char)
            else:
                string += self.current_char
            
            self.next_pos()

        self.next_pos()
        f.write(f'(String,{string},{self.position.line+1})\n')
        return token('String', string, self.position.line+1)

    def isChar(self):
        pass


    def commentChecker(self):   #method checking whether comment is single line or multi line comment
        
        self.next_pos()

        if self.current_char != '$':
            #single line comment method
            a = open(
                r'./token,txt','a'
            )
            singleCommentStr = ''
            position_start = self.position.duplicate()
            
            while self.current_char != None and self.current_char != "\n":

                singleCommentStr += self.current_char
                self.next_pos()
                        
            self.next_pos()
            f.write(f'(Single line comment,{singleCommentStr},{self.position.line+1})\n')
            return token('Single line comment', singleCommentStr, self.position.line+1)

        else:
            #multi line comment method
            a = open(
                r'./token,txt','a'
            )
            multiCommentStr = ''
            position_start = self.position.duplicate()
            
            self.next_pos()

            while self.current_char != None:
                if self.current_char == "$":
                    self.next_pos()
                    if self.current_char == "#": #  #$ $#
                        break

                    else:
                        multiCommentStr = multiCommentStr + '$' + self.current_char
                        self.next_pos()
                        continue

                else:
                    multiCommentStr += self.current_char
                    self.next_pos()
                        
            self.next_pos()
            f.write(f'(Multi line comment,{multiCommentStr},{self.position.line+1})\n')
            return token('Multi line comment', multiCommentStr, self.position.line+1)

# //new this



