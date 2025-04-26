import streamlit as st

# Node and LRUCache classes (same as before)
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

    def show_cache(self):
        curr = self.head.next
        result = []
        while curr != self.tail:
            result.append(f"{curr.key}:{curr.value}")
            curr = curr.next
        return result

# -------------------------------------
# Streamlit Interface
# -------------------------------------

st.title("🔁 LRU Cache Simulator")

# Initialize cache in session_state
if "cache" not in st.session_state:
    st.session_state.cache = None

# Set capacity only once
if st.session_state.cache is None:
    cap = st.number_input("Set Cache Capacity", min_value=1, step=1)
    if st.button("Initialize Cache"):
        st.session_state.cache = LRUCache(cap)
        st.success(f"LRU Cache initialized with capacity {cap}")

else:
    st.subheader("Cache Operations")

    col1, col2 = st.columns(2)
    with col1:
        put_key = st.text_input("Put Key")
        put_val = st.text_input("Put Value")
        if st.button("Put"):
            st.session_state.cache.put(put_key, put_val)
            st.success(f"Added ({put_key}, {put_val})")

    with col2:
        get_key = st.text_input("Get Key")
        if st.button("Get"):
            value = st.session_state.cache.get(get_key)
            if value != -1:
                st.info(f"Value: {value}")
            else:
                st.warning("Key not found!")

    st.markdown("### 🧾 Cache State (MRU → LRU)")
    cache_contents = st.session_state.cache.show_cache()
    if cache_contents:
        st.write(" → ".join(cache_contents))
    else:
        st.write("Cache is empty.")
