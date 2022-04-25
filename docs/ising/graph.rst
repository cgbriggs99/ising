Graphs
======

This module contains classes for dealing with graphs. The idea is to provide facilities for general connections between spins in a matrix.

.. py:module:: ising.graph

	       
.. py:class:: Copyable

   Simply represents a thing with a ``copy`` method.

   .. py:method:: copy()

      Copy the object.
      
      :return: A copy of this object.

   .. py:staticmethod:: iscopyable(obj)

      Returns whether an object has a ``copy`` method.

      :param object obj: The object to determine the copy status.
      :return: True if ``obj.copy()`` is valid. False if it is not.

.. py:class:: Vertex(data, index)

   Represents a vertex. The constructor should not be called. Instead, use the :py:class:`ising.graph.VertexFactory` to create vertices.

   :param object data: Any data to store at the vertex.
   :param int index: The index for this vertex.

   .. py:method:: getdata()

      Gets the data at this vertex.

      :returns: The data stored at this vertex.

   .. py:method:: setdata(data)

      Sets the data at this vertex.

      :param object data: The new data.
      :return: The new data.

   .. py:method:: getindex()

      Gets the index for this vertex.

      :return: The index.

   .. py:method:: _setindex(index)

      Sets the index. Should not be called globally.

      :param int index: The new index.
      :return: The new index.

   .. py:method:: __eq__(other)

      Check for equality.

      :param other: The other thing to check.
      :type other: :py:class:`Vertex` or int
      :return: True if the vertices have the same data, or if the 

   .. py:method:: copy()

      Implementation of :py:meth:`Copyable.copy`.

      :return: A copy of this instance.

   .. py:method:: __str__()

      Returns a string which indicates the index and data.

      :return: String representation.

   .. py:method:: __hash__()

      Returns the index. Useful for making dictionaries. It assumes that the vertex object was produced with the :py:class:`VertexFactory` class, which ensures unique indices.

      :return: The index.

.. py:class:: Edge(index, start, end, [length = 1])

   Represents an edge. Assumed to be directed.

   :param int index: The index for the edge.
   :param Vertex start: The starting vertex.
   :param Vertex end: The ending vertex.
   :param object length: The length of the edge.

   .. py:method:: getstart()

      Returns the starting node.

      :return: The starting node.

   .. py:method:: getend()

      Returns the ending node.

      :return: The ending node.

   .. py:method:: getlength()

      Returns the length.

      :return: The length.

   .. py:method:: setstart(vert)

      Sets the starting vertex to a new value.

      :param Vertex vert: The starting vertex.
      :return: The new starting vertex.

   .. py:method:: setend(vert)

      Sets the ending vertex to a new value.

      :param Vertex vert: The ending vertex.
      :return: The new ending vertex.

   .. py:method:: getindex()

      Returns the index.
      
      :return: The index.

   .. py:method:: _setindex(index)

      Sets the index to a new value. Should not be called globally.

      :param int index: The new index.
      :return: The new index.

   .. py:method:: cantraverse(vert)

      Returns whether the edge can be traversed from the given vertex.

      :param Vertex vert: The starting vertex.
      :return: True if the edge can be traversed. False otherwise.

   .. py:method:: traverse(vert)

      Traverse this edge from the given vertex.

      :param Vertex vert: The starting vertex.
      :return: A tuple containing the ending vertex and the length.

   .. py:method:: __eq__(other)

      Checks to see if two edges are the same: starting from the same point, going to the same point, and having the same length. If the other is not an edge, it is treated like an index, which is compared to the index of the edge.

      :param other: The other thing to compare.
      :type other: Edge or int.
      :return: True if the edges are equal, or if this is the referenced edge. False otherwise.

   .. py:method:: copy()

      Implementation of :py:meth:`Copyable.copy`.

      :return: A copy of this object.

   .. py:method:: __str__()

      Returns a string which has the index of the edge, the start and end nodes, whether it is directed or not, and the length. An example would look like ``[0 : (0: "Vertex Data") -> (1) (200)]``, which has a length of 200, and goes from 0 to 1, with the string ``"Vertex Data"`` attached to vertex 0.

      :return: The string representation.

   .. py:method:: __hash__()

      Returns the index of the edge. Assumes that the edge was made using the :py:class:`graph.EdgeFactory`.

      :return: The index.

.. py:class:: UndirectedEdge(index, start, end, [length = 1])

   Represents an undirected edge. Implements all the same methods as :py:class:`graph.Edge`, but it does not differentiate between the start and end nodes.

.. py:class:: VertexFactory

   Builds vertices, and ensures that they have unique indices. Extends :py:class:`ising.despats.singleton.Singleton`.
   
   .. py:method:: makevertex([data])

      Makes a new vertex.

      :param object data: Data to attach to the vertex.
      :return: A new vertex.

   .. py:method:: makevertex_list(nverts, [data])

      Makes several vertices at a time. If ``data`` is iterable, then the factory method will try to attach each vertex with an entry from the data argument. Otherwise, each vertex will get what is passed in the data argument.

      :param int nverts: Number of vertices.
      :param data: Data to attach to vertices.
      :return: A list of new vertices.

.. py:class:: EdgeFactory

   Builds edges, and ensures that they have unique indices. Extends :py:class:`ising.despats.singleton.Singleton`.

   .. py:method:: makeedge(start, end, [length], [directed])

      Makes a new edge with the given starting node, ending node, and length. Also specifies directed or undirected.

      :param Vertex start: The starting node.
      :param Vertex end: The ending node.
      :param object length: The length. Defaults to 1.
      :param bool directed: True if directed, false if undirected. Defaults to true.
      :return: A new edge.

.. py:class:: Graph(verts, edges)

   Represents a graph with the given edges and vertices.

   .. py:method:: getverts()

      Returns the set of vertices.

      :return: The set of vertices.

   .. py:method:: getvert(index)

      Returns a vertex with the given index, or the vertex that equals the given.
      
      :return: The requested vertex.

   .. py:method:: getedges()

      Returns the set of edges.

      :return: The set of edges.

   .. py:method:: getedge(index, [cutoff])

      Returns an edge which matches the given data. If the data is a tuple, it is expected to look like ``(start, end)`` or ``(start, end, length)``. If it is an index, it will look for an edge with that index. The cutoff parameter is for dealing with floating point lengths, which may have round-off errors.

      :param index: Critera for the edge to be found.
      :type index: tuple or int
      :param float cutoff: The cutoff for floating point equality. Defaults to 1e-6.
      :return: The requested edge.

   .. py:method:: addverts(vert)

      Adds a single vertex or several vertices.

      :param vert: The vertex or vertices.
      :type vert: :py:class:`Vertex` or iterable(:py:class:`Vertex`)
      :return: The set of vertices after adding.

   .. py:method:: addedges(edge)

      Adds a single edge or several edges.

      :param edge: The edge or edges to add.
      :type edge: :py:class:`Edge` or iterable(:py:class:`Edge`)
      :return: The set of edges after adding.

   .. py:method:: hasvertex(vert)

      Returns whether a given vertex is in the graph.

      :param vert: The vertex to check.
      :type vert: :py:class:`Vertex` or int.
      :return: True if the vertex is in the graph. False if not.

   .. py:method:: hasedge(edge)

      Returns whether a given edge is in the graph.

      :param edge: The edge to check.
      :type edge: :py:class:`Edge` or int.
      :return: True if the edge is in the graph. False if not.

   .. py:method:: getneighbors(vert)

      Get the neighbors of a vertex.

      :param vert: The starting vertex.
      :type vert: :py:class:`Vertex` or int.
      :return: A list of tuples. The first element is the end node. The second is the distance. The third is True if the edge is undirected.

.. py:function:: dijkstra(graph, start, end)

   Implementation of Dijkstra's shortest path algorithm for testing purposes.

   :param Graph graph: The graph to use.
   :param Vertex start: The starting node.
   :param Vertex end: The ending node.
   :return: A graph which contains the shortest path.
