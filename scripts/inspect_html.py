#!/usr/bin/env python3
"""Offline HTML evidence inventory. No network, scores, fixes or dependency installs."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=[]; self.headings=[]; self.meta={}; self.canon=[]
        self.in_title=False; self.heading=None; self.json_active=False; self.json_buf=[]; self.json_blocks=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.in_title=True
        if tag in ('h1','h2','h3'): self.heading=[tag,'']
        if tag=='meta': self.meta[(a.get('name') or '').lower()]=a.get('content','')
        if tag=='link' and 'canonical' in a.get('rel','').lower().split(): self.canon.append(a.get('href',''))
        if tag=='script' and a.get('type','').lower()=='application/ld+json': self.json_active=True; self.json_buf=[]
    def handle_data(self, data):
        if self.in_title:self.title.append(data)
        if self.heading is not None:self.heading[1]+=data
        if self.json_active:self.json_buf.append(data)
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if self.heading is not None and tag==self.heading[0]:self.headings.append(self.heading);self.heading=None
        if tag=='script' and self.json_active:self.json_blocks.append(''.join(self.json_buf));self.json_active=False

def inspect(path, url=None):
    p=Page();p.feed(Path(path).read_text(encoding='utf-8'))
    findings=[]
    title=''.join(p.title).strip(); description=p.meta.get('description','').strip()
    if not title: findings.append({'id':'title_missing','state':'confirmed','evidence':'empty or absent title','action':'Describe this page using verified business facts.'})
    if not description:findings.append({'id':'description_missing','state':'review','evidence':'empty or absent description','action':'Consider a factual summary; this is not an indexing requirement.'})
    if len(p.canon)>1:findings.append({'id':'multiple_canonicals','state':'confirmed','evidence':p.canon,'action':'Review the intended representative URL.'})
    if not p.canon:findings.append({'id':'canonical_absent','state':'review','evidence':[],'action':'Check duplicate URL behavior before adding a canonical.'})
    parsed=[]
    for i,s in enumerate(p.json_blocks):
        try:parsed.append(json.loads(s))
        except json.JSONDecodeError as e:findings.append({'id':'jsonld_invalid','state':'confirmed','evidence':f'block {i+1}: {e.msg}','action':'Correct JSON syntax, then verify facts against the visible page.'})
    return {'scope':'offline HTML only; no indexing or citation measurement','title':title,'description':description,'headings':p.headings,'canonical':[urljoin(url,x) if url else x for x in p.canon], 'robots_meta':p.meta.get('robots'), 'jsonld_parsed':parsed,'findings':findings,'ai_visibility':None}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('html');a.add_argument('--url');args=a.parse_args()
    print(json.dumps(inspect(args.html,args.url),ensure_ascii=False,indent=2))
