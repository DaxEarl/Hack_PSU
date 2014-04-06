

from math import log
import sys
import urllib2
import json
import copy

#Functions to handle comment aggrigation and comment sorting
def get_comment_agr(js, lamComments, lamMore):
    comments = []
    def g_comments(comment):
        if comment["kind"]=="more":
            comments.append(lamMore(comment))
            return
        children = comment["data"]["replies"]
        comments.append(lamComments(comment))
        if children == "":
            return
        else:
            for c in children["data"]["children"]:
                g_comments(c)
    for chil in js[1]["data"]["children"]:
        g_comments(chil)
    return comments

#Specific helper for the count subcomments
def get_comments_below(js, lamComments, lamMore):
    comments = []
    def g_comments(comment):
        if comment["kind"]=="more":
            comments.append(lamMore(comment))
            return
        children = comment["data"]["replies"]
        comments.append(lamComments(comment))
        if children == "":
            return
        else:
            for c in children["data"]["children"]:
                g_comments(c)
    for chil in js["data"]["replies"]["data"]["children"]:
        g_comments(chil)
    return comments

def get_subcomment_count(js):
    #Just what it says
    return sum(get_comments_below(js, lambda x: 1, lambda x:x["data"]["count"]))

def get_comment_count(js):
    #Gets the total number of comments given the reddit.com/*+/.json
    return sum(get_comment_agr(js, lambda x: 1, lambda x:x["data"]["count"]))

def get_comments_by_author(js, author):
    #Only gets comments by the given author
    def func(comment):
        if comment["author"]==author:
            return comment
        else:
            return 0
    return filter(lambda x: x!=0, get_comment_agr(js, lambda x:func(x["data"])))

def get_up_for_author(js, author):
    #Gets the number of upvotes for the author
    def func(comment):
        if comment["author"]==author:
            return comment["ups"]-comment["downs"]
        else:
            return 0
    return sum(get_comment_agr(js, lambda x:func(x["data"])))

def get_order_ups(js):
    #Sorts the comments by the number of upvotes
    def sort_helper(comment):
        return comment['data']['ups']
    comments = filter(lambda x:x!=0, get_comment_agr(js, lambda x:x, lambda x:0))
    return sorted(comments, key=sort_helper,reverse=True)

def get_order_contraversial(js):
    #Sorts the comments by the ups plus downs
    def sort_helper(comment):
        return comment['data']['ups']+comment['data']['downs']
    comments = filter(lambda x:x!=0, get_comment_agr(js, lambda x:x, lambda x:0))
    return sorted(comments, key=sort_helper,reverse=True)

def get_order_hot(js):
    #Uses the reddit hot formula to get the list
    def hot(ups, downs, date):
        """The hot formula"""
        s = ups - downs
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = date - 1134028003
        return round(order + sign * seconds / 45000, 7)
    def sort_helper(comment):
        return hot(comment['data']['ups'], comment['data']['downs'], comment['data']['created'])
    comments= filter(lambda x:x!=0, get_comment_agr(js, lambda x:x, lambda x:0))
    return sorted(comments, key=sort_helper,reverse=True)

def get_order_replies(js):
    #Orders them with the ones with the most replies first
    def sort_helper(comment):
        return get_subcomment_count(comment)
    def okay(comment):
        if "replies" not in comment["data"].keys() or comment["data"]["replies"]=='':
            return False
        return True
    comments= filter(lambda x:x!=0, get_comment_agr(js, lambda x:x, lambda x:0))
    comments = filter(lambda x: okay(x),comments)
    return sorted(comments, key=sort_helper,reverse=True)

def kill_replies(comments):
    #dont ever use this because it mutates the list.
    a = []
    for g in comments:
        a.append(g)
    for x in range(len(a)):
        a[x]["data"]["replies"] = ""
    return a


def makeForFrank(clist):
    for k,c in enumerate(clist):
        if "replies" not in c["data"].keys() or c["data"]["replies"]=='':
           # print ":'("
            clist[k]["data"]["repliez"] = 0
        else:
            clist[k]["data"]["repliez"] = get_subcomment_count(clist[k])
            #print clist[k]["data"]["repliez"]
        clist[k] = clist[k]["data"]
    return clist
#makeForFrank(get_order_ups(j))

#jss = open("js.txt", "r").read()
def return_json(js):
    rj = {}
    rj["order_ups"]     = makeForFrank(get_order_ups(js))
    rj["order_contra"]  = makeForFrank(get_order_contraversial(js))
    rj["order_replied"] = makeForFrank(get_order_replies(js))
    rj["order_hot"]     = makeForFrank(get_order_hot(js))
    return rj
