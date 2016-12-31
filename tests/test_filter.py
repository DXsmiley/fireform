import fireform
from fireform.efilter import Filter

entity_box = fireform.entity(fireform.data.box())
entity_nothing = fireform.entity()
entity_tags = fireform.entity(tags = 'one two')

def test_component():
	f = Filter('box')
	f.insert(entity_box)
	f.insert(entity_nothing)
	f.insert(entity_tags)
	assert entity_box in f
	assert entity_nothing not in f
	assert entity_tags not in f

def test_component_exclude():
	f = Filter('-box')
	f.insert(entity_box)
	f.insert(entity_nothing)
	f.insert(entity_tags)
	assert entity_box not in f
	assert entity_nothing in f
	assert entity_tags in f

def test_tag():
	f = Filter('#one')
	f.insert(entity_box)
	f.insert(entity_nothing)
	f.insert(entity_tags)
	assert entity_box not in f
	assert entity_nothing not in f
	assert entity_tags in f

def test_tag_exclude():
	f = Filter('-#one')
	f.insert(entity_box)
	f.insert(entity_nothing)
	f.insert(entity_tags)
	assert entity_box in f
	assert entity_nothing in f
	assert entity_tags not in f

def test_tag_mix():
	f = Filter('#one -#two')
	f.insert(entity_box)
	f.insert(entity_nothing)
	f.insert(entity_tags)
	assert entity_box not in f
	assert entity_nothing not in f
	assert entity_tags not in f
